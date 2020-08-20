---
layout: post
title: Back Garden Weather in CouchDB (Part 3)
date: 2012-01-12 13:46:17.000000000 +00:00
tags:
- couchapp
- couchdb
- javascript
- mustache
- weather
permalink: "/2012/01/12/back-garden-weather-in-couchdb-part-3/"
flickr_user: 'https://www.flickr.com/photos/dexxus/'
flickr_username: "paul bica"
flickr_image: 'https://live.staticflickr.com/5264/5653503758_e82a7437d2_w.jpg'
flickr_imagelink: 'https://www.flickr.com/photos/dexxus/5653503758/'
flickr_imagename: 'almost may'
---
In this series I'm describing how I used a [CouchDB](http://www.couchdb.org)
[CouchApp](http://couchapp.org/page/index) to [display the
weather data](http://www.welwynweather.co.uk) collected by a weather station in my back garden. In the
[first post](/2011/12/02/back-garden-weather-in-couchdb-part-1/) I described CouchApps and how to get
a copy of the site. In the [next post](/2012/01/05/back-garden-weather-in-couchdb-part-2/) we
looked at how to import the data collected by [PyWWS](http://code.google.com/p/pywws/) and how to
render a basic page in a CouchApp. In the post we'll extend the basic page to display real weather data.

Each document in the database is a record of the weather data at a particular point in time. As we want to
display the data over a whole day we need to use a
[`list` function](http://wiki.apache.org/couchdb/Formatting_with_Show_and_List
#Listing_Views_with_CouchDB_0.10_and_later). `list` functions work similarly to the `show` function we saw in
the previous post. Unlike `show` functions `list` functions don't have the document passed in, they can call
a `getRow` function which returns the next row to process. When there are no rows left it returns
`null`.

`show` functions process an individual document and return a single object containing the processed data
and any HTTP headers. Because a `list` function can process a potentially huge number of rows they
return data in a different way. Rather than returning a single object containing the whole response
`list` functions must return their response in chunks. First you need to call the `start`
function, passing in any headers that you want to return. Then you call `send` one or more times to
return parts of your response. A typical `list` function will look like the code below.

```javascript
function (head, req) {
    start({ "headers": { "Content-Type": "text/html" }});n
    send(header);
    while(row = getRow()) {
        data = /* process row */;
        send(row);
    }
    send(footer);
}
```

To process the weather data we can't follow this simple format because we need to split each document up and
display the different measurements separately. Let's look at the code for creating the day page. The complete
code is a bit too long to include in a blog post so checkout the first post in this series to find out how to
get a complete copy of the code.

To start the function we load the templates and code that we need using the CouchApp macros. Next we return
the appropriate `Content-Type` header, and then we create the object that we'll pass to Mustache when
we've processed everything.

```javascript
function(head, req) {
    // !json templates.day
    // !json templates.head
    // !json templates.foot
    // !code vendor/couchapp/lib/mustache.js
    // !code vendor/sprintf-0.6.js
    // !code vendor/date_utils.jsn
    start({ "headers": { "Content-Type": "text/html" }});
    var stash = {
        head: templates.head,
        foot: templates.foot,
        date: req.query.startkey,
    };
```

Next we build a list of the documents that we're processing so we can loop over the documents multiple times.

```javascript
    var rows = [];
    while (row = getRow()) {
        rows.push(row.doc);
    }
```

To calculate maximum and minimum values we need to choose the first value and then run through each piece of
data and see whether it is higher or lower than the current record. As the data collector of the weather
station is separate to the outside sensors occasionally they lose their connection. This means that we can
just pick the value in the first document as our starting value, instead we must choose the first document
where the connection with the outside sensors was made.

```javascript
    if(rows.length > 0) {
        for(var i=0; i<rows.length; i++) {
            if((rows[i].status &amp; 64) == 0) {
                max_temp_out = rows[i].temp_out;
                min_temp_out = rows[i].temp_out;
                max_hum_out = rows[i].hum_out;
                min_hum_out = rows[i].hum_out;
                break;
            }
        }
```

Now we come to the meat of the function. We loop through all of the documents and process them into a series
of arrays, one for each graph that we'll draw on the final page.

```javascript
        for(var i=0; i<rows.length; i++) {
            var temp_out = null;
            var hum_out = null;
            if((rows[i].status & 64) == 0) {
                temp_out = rows[i].temp_out;
                hum_out = rows[i].hum_out;
                total_rain = total_rain + rows[i].rain;
                rainfall.push({ "time": time_text, "rain": rows[i].rain });
                wind.push({ "time": time_text, "wind_ave": rows[i].wind_ave, "wind_gust": rows[i].wind_gust });
            }n
            pressure.push({ "time": time_text, "pressure": rows[i].abs_pressure });
            temps.push({ "time": time_text, "temp_out": temp_out, "temp_in": rows[i].temp_in });
            humidity.push({ "time": time_text, "hum_in": rows[i].hum_in, ";hum_out": hum_out });
        }
    }
```

Lastly we take the `stash`, which in a bit of code I've not included here has the data arrays added to
it, and use it to render the `day` template.

```javascript
    send(Mustache.to_html(templates.day, stash));
    return ""
}
```

Let's look at a part of the `day` template. The page is a fairly standard use of the
[Google Chart Tools](http://code.google.com/apis/chart/) library. In this first snippet we render the
maximum and minimum temperature values, and a blank div that we'll fill with the chart.

```javascript
<h3>Temperature</h3>
<p>Outside: <b>Maximum:</b> {{ max_temp_out }}<sup>o</sup>C <b>Minimum:</b> {{ min_temp_out }}<sup>o</sup>C</p>
<p>Inside: <b>Maximum:</b> {{ max_temp_in }}<sup>o</sup>C <b>Minimum:</b> {{ min_temp_in }}<sup>o</sup>C</p>
<div id="tempchart_div"></div>
```

In the following Javascript function we build a `DataTable` object that we pass to the library to draw
a line chart. The `{{ "{{#temps" }}}}` and `{{ "{{/temps" }}}}` construction is the Mustache way
of looping through the `temps` array. We use it to dynamically write out Javascript code containing the
data we want to render.

```javascript
function drawTempChart() {
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Time');
    data.addColumn('number', 'Outside');
    data.addColumn('number', 'Inside');
    data.addRows([
    {{ "{{#temps" }}}}
        ['{{ time }}', {{ temp_out }}, {{ temp_in }}],
    {{ "{{/temps" }}}}
        null]);
    var chart = new google.visualization.LineChart(document.getElementById('tempchart_div'));
    chart.draw(data, {width: 950, height: 240, title: 'Temperature'});
}
google.setOnLoadCallback(drawTempChart);
```

We now have a page that displays all the collected weather data for a single day. In the next post in this
series we'll look at how to use CouchDB's map/reduce functions to process the data so we can display it by
month and by year.
