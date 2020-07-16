---
layout: post
title: Exposing Docker Ports After The Fact
date: 2017-11-22 12:00:50.000000000 +00:00
type: post
parent_id: '0'
published: true
password: ''
status: publish
categories:
- docker
tags:
- port forwarding
- socat
meta:
  _publicize_job_id: '11711782582'
  _rest_api_client_id: "-1"
  _publicize_done_10916: '1'
  _rest_api_published: '1'
  _wpas_done_8887: '1'
  _publicize_done_external: a:1:{s:7:"twitter";a:1:{i:8887;s:56:"https://twitter.com/andrew_j_w/status/933304818957012993";}}
  publicize_twitter_user: andrew_j_w
author:
  login: andrewjw
  email: andrewjwilkinson@gmail.com
  display_name: Andrew Wilkinson
  first_name: Andrew
  last_name: Wilkinson
permalink: "/2017/11/22/exposing-docker-ports-after-the-fact/"
---
<a href="https://www.flickr.com/photos/mireia/415518987/"><img style="float:right;margin:5px;" src="{{ site.baseurl }}/assets/415518987_a193159cdd_m.jpg" alt="Almacenaje Colorido" /></a><a href="http://www.docker.com">Docker</a> is a great tool for running your applications in a consistent and repeatable environment. One issue that I've come across occasionally is getting data into and out of the environment when it's running.n
In this post I want to talk about exposing ports that are published by applications running inside a container. When you start up the container it's pretty easy to configure the ports you want to expose using the <tt>--publish</tt> or <tt>-p</tt> parameter. It's followed by the internal port number, a colon, and the external port number. For example:n
<pre>docker run --publish 80:8080 myapp</pre>
This will publish port 80 from inside the container as port 8080 on the host.n
This works great if you know want ports you want to expose before you run the container. Once it's running, if you decide you need access to a port, you can't expose it. Unless that is, you cheat.n
<tt><a href="https://linux.die.net/man/1/socat">socat</a></tt> is a very useful command line tool which lets you create tunnels to forward ports. It has many other features, such as forwarding unix sockets to tcp sockets, but we just need to forward a port from an existing container, into a new container and then expose that port to the host.n
Fortunately a Docker container that's only job is to run <tt>socat</tt> already exists, so we just need to pass the right options to forward the remote port, and expose the port.n
I was trying to expose port 61616 from a container called <tt>activemq</tt>, so I ran the following command:n
<pre>docker run -p 61616:61616 alpine/socat tcp-listen:61616,reuseaddr,fork tcp:activemq:61616</pre>
Let's break the command down.n
<tt>docker run -p 61616:61616n
This runs the container and exposes port 61616 on port 61616 on the host.n
<tt>alpine/socat</tt>n
This runs the container alpine/socat.n
<tt>tcp-listen:61616,reuseaddr,fork</tt>n
This is the first parameter that's passed to socat. It specifies that it should listen on port 61616.n
<tt>tcp:activemq:61616</tt>n
This specifies that when an incoming connection arrives it should be connected port 61616 running on container activemq.n
So to summarise, you can run the following command and expose a port while a container is running.n
<pre>docker run -p cport:hostport alpine/socat tcp-listen:cport,reuseaddr,fork tcp:remotehost:remoteport</pre>
<hr />
Photo of <a href="https://www.flickr.com/photos/mireia/415518987/">Almacenaje Colorido</a> by <a href="https://www.flickr.com/photos/mireia/">Mireia mim</a>.</tt>n
