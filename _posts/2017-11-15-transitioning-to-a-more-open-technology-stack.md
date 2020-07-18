---
layout: post
title: Transitioning To A More Open Technology Stack
date: 2017-11-15 12:00:53.000000000 +00:00
type: post
parent_id: '0'
published: true
password: ''
status: publish
categories: []
tags:
- activemq
- java
- jms
meta:
  _publicize_job_id: '11467476585'
  _publicize_done_10916: '1'
  publicize_twitter_user: andrew_j_w
  _rest_api_published: '1'
  _rest_api_client_id: "-1"
  _publicize_done_external: a:1:{s:7:"twitter";a:1:{i:8887;s:56:"https://twitter.com/andrew_j_w/status/930769548726489088";}}
  _wpas_done_8887: '1'
author:
  login: andrewjw
  email: andrewjwilkinson@gmail.com
  display_name: Andrew Wilkinson
  first_name: Andrew
  last_name: Wilkinson
permalink: "/2017/11/15/transitioning-to-a-more-open-technology-stack/"
---
<a href="https://www.flickr.com/photos/gordonfu/8399224122/"><img style="float:right;margin:5px;" src="{{ site.baseurl }}/assets/8399224122_e789348af1_m.jpg" alt="Snowy Postbox" /></a>I'm currently working with some large Java monoliths which talk to each other over ActiveMQ. There are several aspects of the architecture that I'd like to change. Certainly, new production environments (Kubernetes, etc) mean that monoliths are not required because of the overhead of deployment, and the benefits of easier testing and more modular architecture mean that I think the expense of migrating to smaller services will be well worth it. With such an established code base though, the question I'm grappling with is how can we transition to a better, more open technology stack without needing to rewrite from scratch and do a big bang deployment.n
Currently I'm toying with the idea of writing an ActiveMQ to Web Sockets bridge.  Web Sockets are a way of emulating a direct TCP connection in a web browser, although a more normal use case is to send and receive a stream of JSON encoded events. Although Web Sockets were created for use in browsers all languages have libraries available which will allow you to connect to a server.n
ActiveMQ natively supports connecting over Web Sockets, so why would I propose building a bridge application? In our case the messages being exchanged are binary encoded, so you can't decode them unless you're running Java and have the same library used to send the messages. By building an application to act as a bridge you get much more control over the Web Socket API than if you use the native ActiveMQ implementation, so you can tidy up the JSON representations you use and easily make any other improvements to the API that you want.n
Spring is our current Java Framework of choice, which conveniently has a built-in HTTP server which supports Web Sockets. Combining that with our shared library for connecting to ActiveMQ results in a Web Socket server in just a couple of hundred lines of code, and most of that is actually converting the message objects into a nice JSON representation.n
In future posts I'll talk about our progress migrating to a more open environment, but first let's go through how to build the bridge. I've chosen a simple REST API.n
<ul>
<li>GET /topic will return a list of topics.</li>
<li>GET /topic/{topic} returns a single message from the topic (not much use in reality, but useful for testing).</li>
<li>CONNECT /topic/{topic} opens a web socket connection to a topic, which lets you send and receive a stream of events.</li>
</ul>
The first step is to enable web sockets on the right URL.n
<pre>@Configuration
@EnableWebSocket
public class WebSocketConfig implements WebSocketConfigurer {
    @Autowired
    private SocketHandler sockerHandler;

    public void registerWebSocketHandlers(WebSocketHandlerRegistry registry) {
        registry.addHandler(sockerHandler, "/topic/{topic}")
            .setAllowedOrigins("*");
    }
}

</pre>
Next up we set up the normal HTTP end points. Here I'm using two objects to manage the ActiveMQ connections and JSON serialisation/deserialisation. If like us you have shared libraries to do your messaging for you then you can just plug those in, and there are some many JSON serialisers you can just pick your favourite.n
A key thing with this class is to specify the method of the requests so we can use the same URL as we registered for the web sockets without clashing.n
<pre>@Controller
@RequestMapping("/topic")
public class TopicHandler {
    @Autowired
    private JmsConnectionManager jmsConnectionManager;

    @Autowired
    private JsonSerialiser jsonSerialiser;

    @RequestMapping(method = RequestMethod.GET)
    public @ResponseBody List GetTopics() {
        return jsonSerialiser.serialise(jmsConnectionManager.getTopics());
    }

    @RequestMapping(value="/{topic}", method = RequestMethod.GET, headers = "Connection!=Upgrade")
    public @ResponseBody String GetTopic(@PathVariable("topic") String topic) {
        ActiveMqTopicController controller = jmsConnectionManager.getTopicController(topic);

        return jsonSerialiser.serialise(controller.getMessage(), BaseMessage.class);
    }
}
</pre>
Lastly, we handle the web socket connections. There are three methods of TextWebSocketHandler that we need to override. handleTextMessage is called when a message is received from the client, while afterConnectionEstablished and afterConnectionClosed are called at the start and end of the connection. When the connection is established you need to connect to the JMS topic, and start streaming events.n
<pre>@Component
public class SocketHandler extends TextWebSocketHandler {
    @Autowired
    private JmsConnectionManager jmsConnectionManager;

    @Autowired
    private JsonSerialiser jsonSerialiser;

    public SocketHandler() {
    }

    @Override
    public void handleTextMessage(WebSocketSession session, TextMessage message)
            throws InterruptedException {
        BaseMessage jmsMessage = jsonSerialiser.deserialise(message.getPayload(), BaseMessage.class);

        ActiveMqTopicController tc = jmsConnectionManager.getTopicController(getTopic(session));
        tc.publishMessage(jmsMessage);
    }

    @Override
    public void afterConnectionEstablished(WebSocketSession session) throws Exception {
        ActiveMqTopicController tc = jmsConnectionManager.getTopicController(getTopic(session));
        tc.addListener(session);
    }

    @Override
    public void afterConnectionClosed(WebSocketSession session, CloseStatus closeStatus) {
        ActiveMqTopicController tc = jmsConnectionManager.getTopicController(getTopic(session));
        tc.removeListener(session);
    }

    private String getTopic(WebSocketSession session) {
        String path = session.getUri().getRawPath();

        String[] components = path.split("/");

        return components[components.length - 1];
    }
}
</pre>
With this fairly simple code in place, it's dead easy to start integrating other languages, or single page apps running in a web browser into your previously closed messaged based system.n
<hr />
Photo of <a href="https://www.flickr.com/photos/gordonfu/8399224122/">Snowy Postbox</a> by <a href="https://www.flickr.com/photos/gordonfu/">Gordon Fu</a>.n