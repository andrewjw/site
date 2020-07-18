---
layout: post
title: Back Garden Weather in CouchDB (Part 5)
date: 2012-02-10 20:00:07.000000000 +00:00
type: post
parent_id: '0'
published: true
password: ''
status: publish
categories: []
tags:
- couchapp
- couchdb
- weather
meta:
  _edit_last: '364050'
  publicize_results: a:1:{s:7:"twitter";a:1:{i:5934552;a:2:{s:7:"user_id";s:10:"andrew_j_w";s:7:"post_id";s:18:"168061810912661504";}}}
  _wpas_done_twitter: '1'
author:
  login: andrewjw
  email: andrewjwilkinson@gmail.com
  display_name: Andrew Wilkinson
  first_name: Andrew
  last_name: Wilkinson
permalink: "/2012/02/10/back-garden-weather-in-couchdb-part-5/"
---
<a href="http://www.flickr.com/photos/shelley_dave/6818597069/"><img style="float:right;border:0;" src="{{ site.baseurl }}/assets/6818597069_82ed80974b_m.jpg" alt="Snow falling" /></a>After a two week gap the recent <a href="http://www.bbc.co.uk/news/uk-16899453">snow in the UK</a> has inspired me to get back to my series of posts on my weather station website, <a href="http://www.welwynweather.co.uk">WelwynWeather.co.uk</a>. In this post I'll discuss the <a href="http://www.welwynweather.co.uk/records">records page</a>, which shows details such as the highest and lowest temperatures, and the heaviest periods of rain.n
From a <a href="http://andrewwilkinson.wordpress.com/2012/01/12/back-garden-weather-in-couchdb-part-3/">previous post</a> in this series you'll remember that the website is implemented as a <a href="http://couchapp.org/">CouchApp</a>. These are Javascript functions that run inside the CouchDB database, and while they provide quite a lot of flexibility you do need to tailor your code to them.n
On previous pages we have use CouchDB's map/reduce framework to summarise data then used a list function to display the results. The records page could take a similar approach, but there are some drawbacks to that. Unlike the rest of the pages the information on the records page consists of a number of unrelated numbers. While we could create a single map/reduce function to process all of them at once. That function will quickly grow and become unmanageable, so instead we'll calculate the statistics individually and use AJAX to load them dynamically into the page.n
To calculate the minimum indoor temperature we first need to create a simple view to calculate the value. As with all CouchDB views this starts with map function that outputs the parts of the document we are interested in.n
[code language="javascript"]<br />
function(doc) {<br />
    emit(doc._id, { &quot;temp_in&quot;: doc.temp_in, &quot;timestamp&quot;: doc.timestamp });<br />
}<br />
[/code]n
Next we create a reduce function to find the lowest temperature. To do this we simply loop through all the values and select the smallest temperature, recording the timestamp that temperature occurred.n
[code language="javascript"]<br />
function(keys, values, rereduce) {<br />
    var min = values[0].temp_in;<br />
    var min_on = values[0].timestamp;n
    for(var i=0; i&lt;values.length; i++) {<br />
        if(values[i].temp_in &lt; min) {<br />
            min = values[i].temp_in;<br />
            min_on = values[i].timestamp;<br />
        }<br />
    }n
    return { &quot;temp_in&quot;: min, &quot;timestamp&quot;: min_on }<br />
}<br />
[/code]n
The website <a href="http://www.welwynweather.co.uk">welwynweather.co.uk</a> actually points to the Couch <a href="http://wiki.apache.org/couchdb/Rewriting_urls">rewrite document</a>. To make the view available we add a rewrite to expose it to the world. As we want to reduce all documents to a single point we just need to pass <tt>reduce=true</tt> as the query.n
[code language="javascript"]<br />
{<br />
    &quot;from&quot;: &quot;/records/temperature/in/min&quot;,<br />
    &quot;to&quot;: &quot;/_view/records_temp_in_min&quot;,<br />
    &quot;query&quot;: { &quot;reduce&quot;: &quot;true&quot; }<br />
},<br />
[/code]n
Lastly we can use jQuery to load the data and place the values into the DOM at the appropriate place. As CouchDB automatically sends the correct mime type jQuery will automatically decode the JSON data making this function very straightforward.n
[code language="javascript"]<br />
$.getJSON(&quot;records/temperature/in/min&quot;, function (data, textStatus, jqXHR) {<br />
    var row = data.rows[0].value;<br />
    var date = new Date(row.timestamp*1000);<br />
    $(&quot;#min_temp_in&quot;).html(row.temp_in);<br />
    $(&quot;#min_temp_in_date&quot;).html(date.toUTCString());<br />
  });<br />
[/code]n
This approach works well for most of the records that I want to calculate. Where it falls down is when calculating the wettest days and heaviest rain as the data needs to be aggregated before being reduced to a single value. Unfortunately CouchDB does not support this. The issue is that you cannot guarantee that the original documents will be passed to your view in order. In fact it is more likely than not than they won't be. So, to calculate the heaviest periods of rain you would need to build a data structure containing each hour or day and the amount of rain in that period. As the documents are processed the structure would need to be updated and the period with the highest rain found.n
Calculating a complicated structure as the result of your <tt>reduce</tt> function is disallowed by CouchDB, for good reason. An alternative way to find the heaviest periods of rain would be to put the output of the aggregation function into a new database and run another map/reduce function over that to find the heaviest period. Unfortunately CouchDB doesn't support the chaining of views, so this is impossible without using an external program.n
To solve this problem I do the aggregation in CouchDB and the transfer the whole result to the webbrowser and calculate the heaviest period in Javascript. The code to do this is given below. It's very similar to that given above, but includes a loop to cycle over the results and pick the largest value.n
[code language="javascript"]<br />
$.getJSON(&quot;records/rain/wettest&quot;, function (data, textStatus, jqXHR) {<br />
        var max_on = data.rows[0].key;<br />
        var max_rain = data.rows[0].value;<br />
        for(var i=0; i&lt;data.rows.length; i++) {<br />
            if(data.rows[i].value &gt; max_rain) {<br />
                max_on = data.rows[i].key;<br />
                max_rain = data.rows[i].value;<br />
            }<br />
        }<br />
        var date = new Date(max_on*1000);<br />
    $(&quot;#wettest_day&quot;).html(max_rain);<br />
        $(&quot;#wettest_day_date&quot;).html(date.toDateString());<br />
    });<br />
[/code]n
This solution works ok, but as time goes on the dataset gets bigger and bigger and the amount of data that is transferred to the browser will grow and grow. Hopefully in future I'll be able to write another post about changing this to use chained viewed.n
CouchDB is a great document store that is at home the web. The ability to run simple sites right from your database is extremely useful and makes deployment a snap. As with all technology you need to be aware of the limitations of CouchDB and allow for them in your designs. In my case the inability to chain views together is really the only wart in the code. Don't forget you can replicate the database to get the data and use the <tt>couchapp</tt> command to clone a copy of site. See the first post in this series for instructions on how to do this. Please let me know in the comment section below if you find the site useful or have any questions or comments on the code.n
<hr />
Photo of <a href="http://www.flickr.com/photos/shelley_dave/6818597069/">Snow falling</a> by <a href="http://www.flickr.com/photos/shelley_dave/">Dave Gunn</a>.n