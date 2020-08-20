---
layout: post
title: Back Garden Weather in CouchDB (Part 4)
date: 2012-01-20 14:15:19.000000000 +00:00
tags:
- couchapp
- couchdb
- javascript
- mustache
- weather
permalink: "/2012/01/20/back-garden-weather-in-couchdb-part-4/"
flickr_user: 'https://www.flickr.com/photos/13422316@N00/'
flickr_username: "Paul Wordingham"
flickr_image: 'https://live.staticflickr.com/85/243295768_5f556ef303_w.jpg'
flickr_imagelink: 'https://www.flickr.com/photos/13422316@N00/243295768/'
flickr_imagename: 'Weather front'
---
In this series of posts I'm describing how I created a [CouchDB](http://www.couchdb.org)
[CouchApp](http://couchapp.org/page/index) to [display the weather data](http://www.welwynweather.co.uk)
collected by the weather station in my back garden. In the
[previous post](/2012/01/12/back-garden-weather-in-couchdb-part-3/) I showed you how to display a single day's
weather data. In this post we will look at processing the data to display it by month.

The data my weather station collects consists of a record every five minutes. This means that a 31 day month
will consist of 8,928 records. Unless you have space to draw a graph almost nine thousand pixels wide then
there is no point in wasting valuable rending time processing that much data. Reducing the data to one point
per hour gives us a much more manageable 744 data points for a month. A full years worth of weather data
consists of 105,120 records, even reducing it to one point per hour gives us 8760 points. When rendering a
year's worth of data it is clearly worth reducing the data even further, this time to one point per day.

How do we use CouchDB to reduce the data to one point per hour? Fortunately CouchDB's map/reduce architecture
is perfect for this type of processing. CouchDB will also cache the results of the processing automatically so
it only needs to be run once rather than requiring an expensive denormalisation process each time some new
data is uploaded.

First we need to group the five minute weather records together into groups for each hour. We could do this by
taking the unix timestamp of record and rounding to the nearest hour. The problem with this approach is that
the keys are included in the urls. If you can calculate unix timestamps in your head then your maths is better
than mine! To make the urls more friendly we'll use a 
[Javascript implementation of sprintf](http://www.diveintojavascript.com/projects/javascript-sprintf)
to build a human-friendly representation of date and time, excluding the minute component.

```javascript
function(doc) {
    // !code vendor/sprintf-0.6.jsn
    emit(sprintf("%4d-%02d-%02d %02d", doc.year, doc.month, doc.day, doc.hour), doc);
}
```

CouchDB will helpfully group documents with the same key, so all the records from the same hour will be passed
to the reduce function. What you cannot guarantee though is that all the records will be passed in one go,
instead you must ensure that your reduce function can operate on its own output. You can tell whether you are
'rereducing' the output of the reduce function by checking the third parameter to the function.

```javascript
function(keys, values, rereduce) {
    var count = 0;n
    var timestamp = values[0].timestamp;
    var temp_in = 0;
    var temp_out = 0;
    var abs_pressure = 0;
    var rain = 0;n
    var wind_dir = [];
    for(var i=0; i&lt;8; i++) { wind_dir.push({ value: 0}); }
```

To combine the multiple records it makes sense to average most of the values. The exceptions to this are the
amount of rain, which should be summed; the wind direction, which should be a count of the gusts in each
direction, and the wind gust speed which should be the maximum value. Because your reduced function may be
called more than once calculating the average value is not straightforward. If you simply calculate the
average of the values passed in then you will be calculating the average of averages, which is not the same
the average of the full original data. To work around this we calculate the average of the values and store
that with the number of values. Then, when we rereduce, we multiply the average by the number of values and
then average the multiplied value.

In the previous, simplified, code snippet we set up the variables that will hold the averages.n

```javascript
    for(var i=0; i&lt;values.length; i++) {
        var vcount;
        if(rereduce) { vcount = values[i].count } else { vcount = 1 }
```

We now loop through each of the values and work out how many weather records the value we're processing
represents. The initial pass will just represent a single record, but in the rereduce step it will be more.

```javascript
        temp_in = temp_in + values[i].temp_in * vcount;
        temp_out = temp_out + values[i].temp_out * vcount;
        abs_pressure = abs_pressure + values[i].abs_pressure * vcount;
```

Here we build up the total values for temperature and pressure. Later we'll divide these by the number of
records to get the average. The next section adds the rain count up and selects the maximum wind gust.

```javascript
        rain = rain + values[i].rain;
        wind_ave = wind_ave + values[i].wind_ave * vcount;
        if(values[i].wind_gust &gt; wind_gust) { wind_gust = values[i].wind_gust; }
```

So far we've not really had to worry about the possibility of a rereduce, but for wind direction we need to
take it into account. An individual record has a single window direction but for a hourly records we want to
store the count of the number of times each direction was recorded. If we're rereducing we need to loop
through all the directions and combine them.

```javascript
        if(rereduce) {
            for(var j=0; j&lt;8; j++) {
                wind_dir[j]["value"] += values[i].wind_dir[j]["value"];
            }
        } else if(values[i].wind_ave &gt; 0 &amp;&amp; values[i].wind_dir &gt;= 0 &amp;&amp; values[i].wind_dir &lt; 16) {
            wind_dir[Math.floor(values[i].wind_dir/2)]["value"] += 1;
        }
        if(values[i].timestamp &lt; timestamp) { timestamp = values[i].timestamp; }
        count = count + vcount;
    }
```

The final stage is to build the object that we're going to return. This stage is very straightforward, we just
need to divide the numbers we calculated before by the count of the number of records. This gives us the
correct average for these values.

```javascript
    return {
            "count": count,
            "status": status,
            "timestamp": timestamp,
            "temp_in": temp_in / count,
            "temp_out": temp_out / count,
            "abs_pressure": abs_pressure / count,
            "rain": rain,
            "wind_ave": wind_ave / count,
            "wind_gust": wind_gust,
            "wind_dir": wind_dir,
        };
}
```

Now we have averaged the weather data into hourly chunks we can use a `list`, like the one described in
the previous post, to display the data.

In the next and final post in this series I'll discuss the 
[records page](http://www.welwynweather.co.uk/records) on the weather site.
