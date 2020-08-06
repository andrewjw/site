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
In this series I'm describing how I used a <a href="http://www.couchdb.org">CouchDB</a> <a
href="http://couchapp.org/page/index">CouchApp</a> to <a href="http://www.welwynweather.co.uk">display the
weather data</a> collected by a weather station in my back garden. In the <a
href="/2011/12/02/back-garden-weather-in-couchdb-part-1/">first post</a> I described CouchApps and how to get
a copy of the site. In the <a href="/2012/01/05/back-garden-weather-in-couchdb-part-2/">next post</a> we
looked at how to import the data collected by <a href="http://code.google.com/p/pywws/">PyWWS</a> and how to
render a basic page in a CouchApp. In the post we'll extend the basic page to display real weather data.

Each document in the database is a record of the weather data at a particular point in time. As we want to
display the data over a whole day we need to use a <a
href="http://wiki.apache.org/couchdb/Formatting_with_Show_and_List#Listing_Views_with_CouchDB_0.10_and_later"><tt>list</tt>
function</a>. <tt>list</tt> functions work similarly to the <tt>show</tt> function we saw in the previous
post. Unlike <tt>show</tt> functions <tt>list</tt> functions don't have the document passed in, they can call
a <tt>getRow</tt> function which returns the next row to process. When there are no rows left it returns
<tt>null</tt>.

<tt>show</tt> functions process an individual document and return a single object containing the processed data
and any HTTP headers. Because a <tt>list</tt> function can process a potentially huge number of rows they
return data in a different way. Rather than returning a single object containing the whole response
<tt>list</tt> functions must return their response in chunks. First you need to call the <tt>start</tt>
function, passing in any headers that you want to return. Then you call <tt>send</tt> one or more times to
return parts of your response. A typical <tt>list</tt> function will look like the code below.

{% highlight javascript %}
function (head, req) {
    start({ &quot;headers&quot;: { &quot;Content-Type&quot;: &quot;text/html&quot; }});n
    send(header);
    while(row = getRow()) {
        data = /* process row */;
        send(row);
    }
    send(footer);
}
{% endhighlight %}

To process the weather data we can't follow this simple format because we need to split each document up and
display the different measurements separately. Let's look at the code for creating the day page. The complete
code is a bit too long to include in a blog post so checkout the first post in this series to find out how to
get a complete copy of the code.

To start the function we load the templates and code that we need using the CouchApp macros. Next we return
the appropriate <tt>Content-Type</tt> header, and then we create the object that we'll pass to Mustache when
we've processed everything.

{% highlight javascript %}
function(head, req) {
    // !json templates.day
    // !json templates.head
    // !json templates.foot
    // !code vendor/couchapp/lib/mustache.js
    // !code vendor/sprintf-0.6.js
    // !code vendor/date_utils.jsn
    start({ &quot;headers&quot;: { &quot;Content-Type&quot;: &quot;text/html&quot; }});
    var stash = {
        head: templates.head,
        foot: templates.foot,
        date: req.query.startkey,
    };
{% endhighlight %}

Next we build a list of the documents that we're processing so we can loop over the documents multiple times.

{% highlight javascript %}
    var rows = [];
    while (row = getRow()) {
        rows.push(row.doc);
    }
{% endhighlight %}

To calculate maximum and minimum values we need to choose the first value and then run through each piece of
data and see whether it is higher or lower than the current record. As the data collector of the weather
station is separate to the outside sensors occasionally they lose their connection. This means that we can
just pick the value in the first document as our starting value, instead we must choose the first document
where the connection with the outside sensors was made.

{% highlight javascript %}
    if(rows.length &amp;gt; 0) {
        for(var i=0; i&lt;rows.length; i++) {
            if((rows[i].status &amp;amp; 64) == 0) {
                max_temp_out = rows[i].temp_out;
                min_temp_out = rows[i].temp_out;
                max_hum_out = rows[i].hum_out;
                min_hum_out = rows[i].hum_out;
                break;
            }
        }
{% endhighlight %}

Now we come to the meat of the function. We loop through all of the documents and process them into a series
of arrays, one for each graph that we'll draw on the final page.

{% highlight javascript %}
        for(var i=0; i&lt;rows.length; i++) {
            var temp_out = null;
            var hum_out = null;
            if((rows[i].status &amp; 64) == 0) {
                temp_out = rows[i].temp_out;
                hum_out = rows[i].hum_out;
                total_rain = total_rain + rows[i].rain;
                rainfall.push({ &quot;time&quot;: time_text, &quot;rain&quot;: rows[i].rain });
                wind.push({ &quot;time&quot;: time_text, &quot;wind_ave&quot;: rows[i].wind_ave, &quot;wind_gust&quot;: rows[i].wind_gust });
            }n
            pressure.push({ &quot;time&quot;: time_text, &quot;pressure&quot;: rows[i].abs_pressure });
            temps.push({ &quot;time&quot;: time_text, &quot;temp_out&quot;: temp_out, &quot;temp_in&quot;: rows[i].temp_in });
            humidity.push({ &quot;time&quot;: time_text, &quot;hum_in&quot;: rows[i].hum_in, &quot;;hum_out&quot;: hum_out });
        }
    }
{% endhighlight %}

Lastly we take the <tt>stash</tt>, which in a bit of code I've not included here has the data arrays added to
it, and use it to render the <tt>day</tt> template.

{% highlight javascript %}
    send(Mustache.to_html(templates.day, stash));
    return &amp;quot;&amp;quot;
}
{% endhighlight %}

Let's look at a part of the <tt>day</tt> template. The page is a fairly standard use of the <a
href="http://code.google.com/apis/chart/">Google Chart Tools</a> library. In this first snippet we render the
maximum and minimum temperature values, and a blank div that we'll fill with the chart.

{% highlight javascript %}
&lt;h3&gt;Temperature&lt;/h3&gt;
&lt;p&gt;Outside: &lt;b&gt;Maximum:&lt;/b&gt; {{ max_temp_out }}&lt;sup&gt;o&lt;/sup&gt;C &lt;b&gt;Minimum:&lt;/b&gt; {{ min_temp_out }}&lt;sup&gt;o&lt;/sup&gt;C&lt;/p&gt;
&lt;p&gt;Inside: &lt;b&gt;Maximum:&lt;/b&gt; {{ max_temp_in }}&lt;sup&gt;o&lt;/sup&gt;C &lt;b&gt;Minimum:&lt;/b&gt; {{ min_temp_in }}&lt;sup&gt;o&lt;/sup&gt;C&lt;/p&gt;
&lt;div id=&quot;tempchart_div&quot;&gt;&lt;/div&gt;
{% endhighlight %}

In the following Javascript function we build a <tt>DataTable</tt> object that we pass to the library to draw
a line chart. The <tt>{{ "{{#temps" }}}}</tt> and <tt>{{ "{{/temps" }}}}</tt> construction is the Mustache way
of looping through the <tt>temps</tt> array. We use it to dynamically write out Javascript code containing the
data we want to render.

{% highlight javascript %}
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
{% endhighlight %}

We now have a page that displays all the collected weather data for a single day. In the next post in this
series we'll look at how to use CouchDB's map/reduce functions to process the data so we can display it by
month and by year.
