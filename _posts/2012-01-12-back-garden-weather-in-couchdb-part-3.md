---
layout: post
title: Back Garden Weather in CouchDB (Part 3)
date: 2012-01-12 13:46:17.000000000 +00:00
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
  publicize_results: a:1:{s:7:"twitter";a:1:{i:5934552;a:2:{s:7:"user_id";s:10:"andrew_j_w";s:7:"post_id";s:18:"157458380582170624";}}}
  _wpas_done_twitter: '1'
author:
  login: andrewjw
  email: andrewjwilkinson@gmail.com
  display_name: Andrew Wilkinson
  first_name: Andrew
  last_name: Wilkinson
permalink: "/2012/01/12/back-garden-weather-in-couchdb-part-3/"
---
<a href="http://www.flickr.com/photos/dexxus/5653503758/"><img style="float:right;border:0;" src="{{ site.baseurl }}/assets/5653503758_077615716a_m.jpg" alt="almost may" /></a>In this series I'm describing how I used a <a href="http://www.couchdb.org">CouchDB</a> <a href="http://couchapp.org/page/index">CouchApp</a> to <a href="http://www.welwynweather.co.uk">display the weather data</a> collected by a weather station in my back garden. In the <a href="http://andrewwilkinson.wordpress.com/2011/12/02/back-garden-weather-in-couchdb-part-1/">first post</a> I described CouchApps and how to get a copy of the site. In the <a href="http://andrewwilkinson.wordpress.com/2012/01/05/back-garden-weather-in-couchdb-part-2/">next post</a> we looked at how to import the data collected by <a href="http://code.google.com/p/pywws/">PyWWS</a> and how to render a basic page in a CouchApp. In the post we'll extend the basic page to display real weather data.n
Each document in the database is a record of the weather data at a particular point in time. As we want to display the data over a whole day we need to use a <a href="http://wiki.apache.org/couchdb/Formatting_with_Show_and_List#Listing_Views_with_CouchDB_0.10_and_later"><tt>list</tt> function</a>. <tt>list</tt> functions work similarly to the <tt>show</tt> function we saw in the previous post. Unlike <tt>show</tt> functions <tt>list</tt> functions don't have the document passed in, they can call a <tt>getRow</tt> function which returns the next row to process. When there are no rows left it returns <tt>null</tt>.n
<tt>show</tt> functions process an individual document and return a single object containing the processed data and any HTTP headers. Because a <tt>list</tt> function can process a potentially huge number of rows they return data in a different way. Rather than returning a single object containing the whole response <tt>list</tt> functions must return their response in chunks. First you need to call the <tt>start</tt> function, passing in any headers that you want to return. Then you call <tt>send</tt> one or more times to return parts of your response. A typical <tt>list</tt> function will look like the code below.n
[code language="javascript"]<br />
function (head, req) {<br />
    start({ &quot;headers&quot;: { &quot;Content-Type&quot;: &quot;text/html&quot; }});n
    send(header);<br />
    while(row = getRow()) {<br />
        data = /* process row */;<br />
        send(row);<br />
    }<br />
    send(footer);<br />
}<br />
[/code]n
To process the weather data we can't follow this simple format because we need to split each document up and display the different measurements separately. Let's look at the code for creating the day page. The complete code is a bit too long to include in a blog post so checkout the first post in this series to find out how to get a complete copy of the code.n
To start the function we load the templates and code that we need using the CouchApp macros. Next we return the appropriate <tt>Content-Type</tt> header, and then we create the object that we'll pass to Mustache when we've processed everything.n
[code language="javascript"]<br />
function(head, req) {<br />
    // !json templates.day<br />
    // !json templates.head<br />
    // !json templates.foot<br />
    // !code vendor/couchapp/lib/mustache.js<br />
    // !code vendor/sprintf-0.6.js<br />
    // !code vendor/date_utils.jsn
    start({ &quot;headers&quot;: { &quot;Content-Type&quot;: &quot;text/html&quot; }});n
    var stash = {<br />
        head: templates.head,<br />
        foot: templates.foot,<br />
        date: req.query.startkey,<br />
    };<br />
[/code]n
Next we build a list of the documents that we're processing so we can loop over the documents multiple times.n
[code language="javascript"]<br />
    var rows = [];<br />
    while (row = getRow()) {<br />
        rows.push(row.doc);<br />
    }<br />
[/code]n
To calculate maximum and minimum values we need to choose the first value and then run through each piece of data and see whether it is higher or lower than the current record. As the data collector of the weather station is separate to the outside sensors occasionally they lose their connection. This means that we can just pick the value in the first document as our starting value, instead we must choose the first document where the connection with the outside sensors was made.n
[code language="javascript"]<br />
    if(rows.length &amp;gt; 0) {<br />
        for(var i=0; i&lt;rows.length; i++) {<br />
            if((rows[i].status &amp;amp; 64) == 0) {<br />
                max_temp_out = rows[i].temp_out;<br />
                min_temp_out = rows[i].temp_out;<br />
                max_hum_out = rows[i].hum_out;<br />
                min_hum_out = rows[i].hum_out;n
                break;<br />
            }<br />
        }<br />
[/code]n
Now we come to the meat of the function. We loop through all of the documents and process them into a series of arrays, one for each graph that we'll draw on the final page.n
[code language="javascript"]<br />
        for(var i=0; i&lt;rows.length; i++) {<br />
            var temp_out = null;<br />
            var hum_out = null;<br />
            if((rows[i].status &amp; 64) == 0) {<br />
                temp_out = rows[i].temp_out;<br />
                hum_out = rows[i].hum_out;n
                total_rain = total_rain + rows[i].rain;<br />
                rainfall.push({ &quot;time&quot;: time_text, &quot;rain&quot;: rows[i].rain });n
                wind.push({ &quot;time&quot;: time_text, &quot;wind_ave&quot;: rows[i].wind_ave, &quot;wind_gust&quot;: rows[i].wind_gust });n
            }n
            pressure.push({ &quot;time&quot;: time_text, &quot;pressure&quot;: rows[i].abs_pressure });n
            temps.push({ &quot;time&quot;: time_text, &quot;temp_out&quot;: temp_out, &quot;temp_in&quot;: rows[i].temp_in });n
            humidity.push({ &quot;time&quot;: time_text, &quot;hum_in&quot;: rows[i].hum_in, &quot;;hum_out&quot;: hum_out });<br />
        }<br />
    }<br />
[/code]n
Lastly we take the <tt>stash</tt>, which in a bit of code I've not included here has the data arrays added to it, and use it to render the <tt>day</tt> template.n
[code language="javascript"]<br />
    send(Mustache.to_html(templates.day, stash));n
    return &amp;quot;&amp;quot;;<br />
}<br />
[/code]n
Let's look at a part of the <tt>day</tt> template. The page is a fairly standard use of the <a href="http://code.google.com/apis/chart/">Google Chart Tools</a> library. In this first snippet we render the maximum and minimum temperature values, and a blank div that we'll fill with the chart.n
[code language="html"]<br />
&lt;h3&gt;Temperature&lt;/h3&gt;n
&lt;p&gt;Outside: &lt;b&gt;Maximum:&lt;/b&gt; {{ max_temp_out }}&lt;sup&gt;o&lt;/sup&gt;C &lt;b&gt;Minimum:&lt;/b&gt; {{ min_temp_out }}&lt;sup&gt;o&lt;/sup&gt;C&lt;/p&gt;<br />
&lt;p&gt;Inside: &lt;b&gt;Maximum:&lt;/b&gt; {{ max_temp_in }}&lt;sup&gt;o&lt;/sup&gt;C &lt;b&gt;Minimum:&lt;/b&gt; {{ min_temp_in }}&lt;sup&gt;o&lt;/sup&gt;C&lt;/p&gt;n
&lt;div id=&quot;tempchart_div&quot;&gt;&lt;/div&gt;<br />
[/code]n
In the following Javascript function we build a <tt>DataTable</tt> object that we pass to the library to draw a line chart. The <tt>{{#temps}}</tt> and <tt>{{/temps}}</tt> construction is the Mustache way of looping through the <tt>temps</tt> array. We use it to dynamically write out Javascript code containing the data we want to render.n
[code language="javascript"]<br />
function drawTempChart() {<br />
    var data = new google.visualization.DataTable();<br />
    data.addColumn('string', 'Time');<br />
    data.addColumn('number', 'Outside');<br />
    data.addColumn('number', 'Inside');n
    data.addRows([<br />
    {{#temps}}<br />
        ['{{ time }}', {{ temp_out }}, {{ temp_in }}],<br />
    {{/temps}}<br />
        null]);n
    var chart = new google.visualization.LineChart(document.getElementById('tempchart_div'));<br />
    chart.draw(data, {width: 950, height: 240, title: 'Temperature'});<br />
}<br />
google.setOnLoadCallback(drawTempChart);<br />
[/code]n
We now have a page that displays all the collected weather data for a single day. In the next post in this series we'll look at how to use CouchDB's map/reduce functions to process the data so we can display it by month and by year.n
<hr />
Photo of <a href="http://www.flickr.com/photos/dexxus/5653503758/">almost may</a> by <a href="http://www.flickr.com/photos/dexxus/">paul bica</a>.n