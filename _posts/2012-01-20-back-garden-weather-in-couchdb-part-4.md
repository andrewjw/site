---
layout: post
title: Back Garden Weather in CouchDB (Part 4)
date: 2012-01-20 14:15:19.000000000 +00:00
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
  publicize_results: a:1:{s:7:"twitter";a:1:{i:5934552;a:2:{s:7:"user_id";s:10:"andrew_j_w";s:7:"post_id";s:18:"160364815351689217";}}}
  _wpas_done_twitter: '1'
author:
  login: andrewjw
  email: andrewjwilkinson@gmail.com
  display_name: Andrew Wilkinson
  first_name: Andrew
  last_name: Wilkinson
permalink: "/2012/01/20/back-garden-weather-in-couchdb-part-4/"
---
<a href="http://www.flickr.com/photos/13422316@N00/243295768/"><img style="float:right;border:0;" src="{{ site.baseurl }}/assets/243295768_5f556ef303_m.jpg" alt="Weather front" /></a>In this series of posts I'm describing how I created a <a href="http://www.couchdb.org">CouchDB</a> <a href="http://couchapp.org/page/index">CouchApp</a> to <a href="http://www.welwynweather.co.uk">display the weather data</a> collected by the weather station in my back garden. In the <a href="http://andrewwilkinson.wordpress.com/2012/01/12/back-garden-weather-in-couchdb-part-3/">previous post</a> I showed you how to display a single day's weather data. In this post we will look at processing the data to display it by month.n
The data my weather station collects consists of a record every five minutes. This means that a 31 day month will consist of 8,928 records. Unless you have space to draw a graph almost nine thousand pixels wide then there is no point in wasting valuable rending time processing that much data. Reducing the data to one point per hour gives us a much more manageable 744 data points for a month. A full years worth of weather data consists of 105,120 records, even reducing it to one point per hour gives us 8760 points. When rendering a year's worth of data it is clearly worth reducing the data even further, this time to one point per day.n
How do we use CouchDB to reduce the data to one point per hour? Fortunately CouchDB's map/reduce architecture is perfect for this type of processing. CouchDB will also cache the results of the processing automatically so it only needs to be run once rather than requiring an expensive denormalisation process each time some new data is uploaded.n
First we need to group the five minute weather records together into groups for each hour. We could do this by taking the unix timestamp of record and rounding to the nearest hour. The problem with this approach is that the keys are included in the urls. If you can calculate unix timestamps in your head then your maths is better than mine! To make the urls more friendly we'll use a <a href="http://www.diveintojavascript.com/projects/javascript-sprintf">Javascript implementation of sprintf</a> to build a human-friendly representation of date and time, excluding the minute component.n
[code language="javascript"]<br />
function(doc) {<br />
    // !code vendor/sprintf-0.6.jsn
    emit(sprintf(&quot;%4d-%02d-%02d %02d&quot;, doc.year, doc.month, doc.day, doc.hour), doc);<br />
}<br />
[/code]n
CouchDB will helpfully group documents with the same key, so all the records from the same hour will be passed to the reduce function. What you cannot guarantee though is that all the records will be passed in one go, instead you must ensure that your reduce function can operate on its own output. You can tell whether you are 'rereducing' the output of the reduce function by checking the third parameter to the function.n
[code language="javascript"]<br />
function(keys, values, rereduce) {<br />
    var count = 0;n
    var timestamp = values[0].timestamp;<br />
    var temp_in = 0;<br />
    var temp_out = 0;<br />
    var abs_pressure = 0;<br />
    var rain = 0;n
    var wind_dir = [];<br />
    for(var i=0; i&lt;8; i++) { wind_dir.push({ value: 0}); }<br />
[/code]n
To combine the multiple records it makes sense to average most of the values. The exceptions to this are the amount of rain, which should be summed; the wind direction, which should be a count of the gusts in each direction, and the wind gust speed which should be the maximum value. Because your reduced function may be called more than once calculating the average value is not straightforward. If you simply calculate the average of the values passed in then you will be calculating the average of averages, which is not the same the average of the full original data. To work around this we calculate the average of the values and store that with the number of values. Then, when we rereduce, we multiply the average by the number of values and then average the multiplied value.n
In the previous, simplified, code snippet we set up the variables that will hold the averages.n
[code language="javascript"]    for(var i=0; i&lt;values.length; i++) {<br />
        var vcount;<br />
        if(rereduce) { vcount = values[i].count } else { vcount = 1 }<br />
[/code]n
We now loop through each of the values and work out how many weather records the value we're processing represents. The initial pass will just represent a single record, but in the rereduce step it will be more.n
[code language="javascript"]        temp_in = temp_in + values[i].temp_in * vcount;<br />
        temp_out = temp_out + values[i].temp_out * vcount;<br />
        abs_pressure = abs_pressure + values[i].abs_pressure * vcount;<br />
[/code]n
Here we build up the total values for temperature and pressure. Later we'll divide these by the number of records to get the average. The next section adds the rain count up and selects the maximum wind gust.n
[code language="javascript"]<br />
        rain = rain + values[i].rain;n
        wind_ave = wind_ave + values[i].wind_ave * vcount;<br />
        if(values[i].wind_gust &gt; wind_gust) { wind_gust = values[i].wind_gust; }<br />
[/code]n
So far we've not really had to worry about the possibility of a rereduce, but for wind direction we need to take it into account. An individual record has a single window direction but for a hourly records we want to store the count of the number of times each direction was recorded. If we're rereducing we need to loop through all the directions and combine them.n
[code language="javascript"]<br />
        if(rereduce) {<br />
            for(var j=0; j&lt;8; j++) {<br />
                wind_dir[j][&quot;value&quot;] += values[i].wind_dir[j][&quot;value&quot;];<br />
            }<br />
        } else if(values[i].wind_ave &gt; 0 &amp;&amp; values[i].wind_dir &gt;= 0 &amp;&amp; values[i].wind_dir &lt; 16) {<br />
            wind_dir[Math.floor(values[i].wind_dir/2)][&quot;value&quot;] += 1;<br />
        }n
        if(values[i].timestamp &lt; timestamp) { timestamp = values[i].timestamp; }<br />
        count = count + vcount;<br />
    }<br />
[/code]n
The final stage is to build the object that we're going to return. This stage is very straightforward, we just need to divide the numbers we calculated before by the count of the number of records. This gives us the correct average for these values.n
[code language="javascript"]    return {<br />
            &quot;count&quot;: count,<br />
            &quot;status&quot;: status,<br />
            &quot;timestamp&quot;: timestamp,<br />
            &quot;temp_in&quot;: temp_in / count,<br />
            &quot;temp_out&quot;: temp_out / count,<br />
            &quot;abs_pressure&quot;: abs_pressure / count,<br />
            &quot;rain&quot;: rain,<br />
            &quot;wind_ave&quot;: wind_ave / count,<br />
            &quot;wind_gust&quot;: wind_gust,<br />
            &quot;wind_dir&quot;: wind_dir,<br />
        };<br />
}<br />
[/code]n
Now we have averaged the weather data into hourly chunks we can use a <tt>list</tt>, like the one described in the previous post, to display the data.n
In the next and final post in this series I'll discuss the <a href="http://www.welwynweather.co.uk/records">records page</a> on the weather site.n
<hr />
Photo of <a href="http://www.flickr.com/photos/13422316@N00/243295768/">Weather front</a> by <a href="http://www.flickr.com/photos/13422316@N00/">Paul Wordingham</a>.n
