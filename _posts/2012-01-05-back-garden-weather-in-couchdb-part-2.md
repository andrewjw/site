---
layout: post
title: Back Garden Weather in CouchDB (Part 2)
date: 2012-01-05 13:58:04.000000000 +00:00
tags:
- couchapp
- couchdb
- javascript
- mustache
- weather
permalink: "/2012/01/05/back-garden-weather-in-couchdb-part-2/"
flickr_user: 'https://www.flickr.com/photos/scelera/'
flickr_username: "samantha celera"
flickr_image: 'https://live.staticflickr.com/2073/2226758824_a5df2b2629_w.jpg'
flickr_imagelink: 'https://www.flickr.com/photos/scelera/2226758824/'
flickr_imagename: 'its raining..its pouring'
---
In my [last post](2011/12/02/back-garden-weather-in-couchdb-part-1/) I described the new
CouchDB-based [website](http://www.welwynweather.co.uk) I have built to display the weather data
collected from the weather station in my back garden. In this post I'll describe to import the data into
CouchDB and the basics of rendering a page with a [CouchApp](http://couchapp.org).

[PyWWS](http://code.google.com/p/pywws/) writes out the raw data it collected into a series of CSV
files, one per day. These are stored in two nested directory, the first being the year, the second being
`year-month`. To collect the data I use PyWWS's live logging mode, which consists of a process
constantly running, talking to the data collector. Every five minutes it writes a new row into today's CSV
file. Another process then runs every five minutes to read the new row, and import it into the database.

Because CouchDB stores its data using an append only format you should aim to avoid unnecessary updates. The
simplest way to write the import script would be to import each day's data every five minutes. This would
cause the database to balloon in size, so instead we query the database to find the last update time and
import everything after than. Each update is stored as a separate document in the database, with the
`timestamp` attribute containing the unix timestamp of the update.

The map code to get the most recent update is quite simple, we just need to emit the timestamp for each
update. The reason the timestamp is emitted as the key is so we can filter the range of updates. It is also
emitted as the value so we can use the timestamp in the reduce function.

```javascript
function(doc) {
    emit(doc.timestamp, doc.timestamp);
}
```

The reduce function is a fairly simple way to calculate the maximum value of the keys. I've mostly included it
here for completeness.

```javascript
function(keys, values, rereduce) {
    if(values.length == 0) {
        return 0;
    }
    var m = values[0];
    for(var i=0; i&lt;values.length; i++) {
        if(values[i] &gt; m) { m = values[i]; }
    }
    return m;
}
```

You'll find the import script that I use in the directory you cloned in the previous post, when you got a copy
of the website.

So, we've got some data in our database. How do we display it on a webpage? First, let's consider the basics
of rendering a webpage.

CouchDB has two ways to display formatted data, 
[show and list](http://wiki.apache.org/couchdb/Formatting_with_Show_and_List) functions. Show
functions allow you to format a single documents, for example a blog post. List functions allow you to format
a group of documents, such as a the comments on a post. Because viewing a single piece of weather data is not
interesting the weather site only uses list functions. To get started let's create a simple Show function, as
these are simpler.

CouchApp doesn't come with a templating library, but a common one to use is 
[Mustache](http://mustache.github.com/). The syntax is superficially like Django templates, but in
reality it is far less powerful. For a simple website like this, Mustache is perfect.

In the `show` directory of your CouchApp create a new file, `test.js`. As with the map/reduce
functions this file contains an anonymous function. In this case the function takes two parameters, the
document and the request obejct, and returns an object containing the response body and any headers.

```javascript
function (doc, req) {
    // !json templates.records
    // !json templates.head
    // !json templates.foot
    // !code vendor/couchapp/lib/mustache.js
```

The function begins with some magic comments. These are commands to CouchDB which includes the referenced code
or data in the function. This allows you to keep shared data separate from the functions that uses it.

The first `[!json](http://guide.couchdb.org/draft/show.html#json)` command causes the
compiler to load the file `templates/records.*` and add it to a `templates` objects, under the
`records` attribute.

The `[!code](http://guide.couchdb.org/draft/show.html#code)` command works similarly, but in
loads the specified file and includes the code in your function. Here we load the Mustache library, but I have
also used the function to load [a
javascript implementation of `sprintf`](http://www.diveintojavascript.com/projects/javascript-sprintf). You might want to load some of your own common code using
this method.

```javascript
    var stash = {
        head: templates.head,
        foot: templates.foot
    };
    return { body: Mustache.to_html(templates.records, stash), headers: { &quot;Content-Type&quot;: &quot;text/html&quot; } };
}
```

Firstly we build an object containing the data we want to use in our template. As Mustache doesn't allow you
to extend templates we need to pass the header and footer HTML code in as data.

As mentioned the return type of a `show function` is a object containing the HTML and any HTTP headers.
We only want to include the content type of the page, but you could return any HTTP header in a similar
fashion. To generate the HTML we call the `to_html` function provided by Mustache, passing the template
and the data object we prepared earlier.

Now we have data in our database and can create simple pages using a CouchApp we can move on to showing real
data. In the next post I will describe the list functions use to show summarized day and month weather
information.
