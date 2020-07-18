---
layout: post
title: Back Garden Weather in CouchDB (Part 2)
date: 2012-01-05 13:58:04.000000000 +00:00
type: post
parent_id: '0'
published: true
password: ''
status: publish
categories: []
tags:
- couchapp
- couchdb
- javascript
- mustache
- weather
meta:
  _edit_last: '364050'
  publicize_results: a:1:{s:7:"twitter";a:1:{i:5934552;a:2:{s:7:"user_id";s:10:"andrew_j_w";s:7:"post_id";s:18:"154924630677782528";}}}
  _wpas_done_twitter: '1'
author:
  login: andrewjw
  email: andrewjwilkinson@gmail.com
  display_name: Andrew Wilkinson
  first_name: Andrew
  last_name: Wilkinson
permalink: "/2012/01/05/back-garden-weather-in-couchdb-part-2/"
---
<a href="http://www.flickr.com/photos/scelera/2226758824/"><img style="float:right;border:0;" src="{{ site.baseurl }}/assets/2226758824_a5df2b2629_m.jpg" alt="its raining..its pouring" /></a>In my <a href="http://andrewwilkinson.wordpress.com/2011/12/02/back-garden-weather-in-couchdb-part-1/">last post</a> I described the new CouchDB-based <a href="http://www.welwynweather.co.uk">website</a> I have built to display the weather data collected from the weather station in my back garden. In this post I'll describe to import the data into CouchDB and the basics of rendering a page with a <a href="http://couchapp.org">CouchApp</a>.n
<a href="http://code.google.com/p/pywws/">PyWWS</a> writes out the raw data it collected into a series of CSV files, one per day. These are stored in two nested directory, the first being the year, the second being <tt>year-month</tt>. To collect the data I use PyWWS's live logging mode, which consists of a process constantly running, talking to the data collector. Every five minutes it writes a new row into today's CSV file. Another process then runs every five minutes to read the new row, and import it into the database.n
Because CouchDB stores its data using an append only format you should aim to avoid unnecessary updates. The simplest way to write the import script would be to import each day's data every five minutes. This would cause the database to balloon in size, so instead we query the database to find the last update time and import everything after than. Each update is stored as a separate document in the database, with the <tt>timestamp</tt> attribute containing the unix timestamp of the update. n
The map code to get the most recent update is quite simple, we just need to emit the timestamp for each update. The reason the timestamp is emitted as the key is so we can filter the range of updates. It is also emitted as the value so we can use the timestamp in the reduce function.n
[code]<br />
function(doc) {<br />
    emit(doc.timestamp, doc.timestamp);<br />
}<br />
[/code]n
The reduce function is a fairly simple way to calculate the maximum value of the keys. I've mostly included it here for completeness.n
[code]<br />
function(keys, values, rereduce) {<br />
    if(values.length == 0) {<br />
        return 0;<br />
    }n
    var m = values[0];n
    for(var i=0; i&lt;values.length; i++) {<br />
        if(values[i] &gt; m) { m = values[i]; }<br />
    }n
    return m;<br />
}<br />
[/code]n
You'll find the import script that I use in the directory you cloned in the previous post, when you got a copy of the website.n
So, we've got some data in our database. How do we display it on a webpage? First, let's consider the basics of rendering a webpage.n
CouchDB has two ways to display formatted data, <a href="http://wiki.apache.org/couchdb/Formatting_with_Show_and_List">show and list</a> functions. Show functions allow you to format a single documents, for example a blog post. List functions allow you to format a group of documents, such as a the comments on a post. Because viewing a single piece of weather data is not interesting the weather site only uses list functions. To get started let's create a simple Show function, as these are simpler.n
CouchApp doesn't come with a templating library, but a common one to use is <a href="http://mustache.github.com/">Mustache</a>. The syntax is superficially like Django templates, but in reality it is far less powerful. For a simple website like this, Mustache is perfect.n
In the <tt>show</tt> directory of your CouchApp create a new file, <tt>test.js</tt>. As with the map/reduce functions this file contains an anonymous function. In this case the function takes two parameters, the document and the request obejct, and returns an object containing the response body and any headers.n
[code]<br />
function (doc, req) {<br />
    // !json templates.records<br />
    // !json templates.head<br />
    // !json templates.foot<br />
    // !code vendor/couchapp/lib/mustache.js<br />
[/code]n
The function begins with some magic comments. These are commands to CouchDB which includes the referenced code or data in the function. This allows you to keep shared data separate from the functions that uses it.n
The first <tt><a href="http://guide.couchdb.org/draft/show.html#json">!json</a></tt> command causes the compiler to load the file <tt>templates/records.*</tt> and add it to a <tt>templates</tt> objects, under the <tt>records</tt> attribute.n
The <tt><a href="http://guide.couchdb.org/draft/show.html#code">!code</a></tt> command works similarly, but in loads the specified file and includes the code in your function. Here we load the Mustache library, but I have also used the function to load <a href="http://www.diveintojavascript.com/projects/javascript-sprintf">a javascript implementation of <tt>sprintf</tt></a>. You might want to load some of your own common code using this method.n
[code]<br />
    var stash = {<br />
        head: templates.head,<br />
        foot: templates.foot<br />
    };n
    return { body: Mustache.to_html(templates.records, stash), headers: { &quot;Content-Type&quot;: &quot;text/html&quot; } };<br />
}<br />
[/code]n
Firstly we build an object containing the data we want to use in our template. As Mustache doesn't allow you to extend templates we need to pass the header and footer HTML code in as data.n
As mentioned the return type of a <tt>show function</tt> is a object containing the HTML and any HTTP headers. We only want to include the content type of the page, but you could return any HTTP header in a similar fashion. To generate the HTML we call the <tt>to_html</tt> function provided by Mustache, passing the template and the data object we prepared earlier.n
Now we have data in our database and can create simple pages using a CouchApp we can move on to showing real data. In the next post I will describe the list functions use to show summarized day and month weather information.n
<hr />
Photo of <a href="http://www.flickr.com/photos/scelera/2226758824/">its raining..its pouring</a> by <a href="http://www.flickr.com/photos/scelera/">samantha celera</a>.n