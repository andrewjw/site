---
layout: post
title: Back Garden Weather in CouchDB (Part 1)
date: 2011-12-02 12:00:55.000000000 +00:00
type: post
parent_id: '0'
published: true
password: ''
status: publish
categories: []
tags:
- couchdb
- pywws
- weather
meta:
  _edit_last: '364050'
  publicize_results: a:1:{s:7:"twitter";a:1:{i:5934552;a:2:{s:7:"user_id";s:10:"andrew_j_w";s:7:"post_id";s:18:"142574228733038593";}}}
  _wpas_done_twitter: '1'
  _oembed_7b2cd1757ce055bcf4774664df3da461: "{{unknown}}"
  _oembed_40aa0d52e891d127228da39a72eec10e: "{{unknown}}"
  _oembed_e4ad14e5328dca135b023c3b4fa556a5: "{{unknown}}"
  _oembed_dc939a7eddebc8745a59a5d4845a133b: "{{unknown}}"
  _oembed_f7b16d2dc58c4780f2103f8d5535b48a: "{{unknown}}"
  _oembed_3a7a1a445398d83e772991931e7245c2: "{{unknown}}"
  _oembed_f2c74edff326c9e653a2604f57346e50: "{{unknown}}"
  _oembed_66d44b1e77f5d8f970988a9482370a4b: "{{unknown}}"
author:
  login: andrewjw
  email: andrewjwilkinson@gmail.com
  display_name: Andrew Wilkinson
  first_name: Andrew
  last_name: Wilkinson
permalink: "/2011/12/02/back-garden-weather-in-couchdb-part-1/"
---
<a href="http://www.flickr.com/photos/aigle_dore/4650548165/"><img style="float:right;border:0;" src="{{ site.baseurl }}/assets/4650548165_b3bb04b3ee_m.jpg" alt="Rain" /></a>When she was younger my wife wanted to be a meteorologist. That didn't pan out, but our recent move found us with a garden, which we've not had before. This gave me the opportunity to buy her <a href="http://smartweather.co.uk/product.php?productid=16144&amp;cat=249&amp;page=1">a weather station</a>. I didn't just choose any old station though, I wanted one that did wind and rain as well as the usual temperature, pressure and humidity. And, the deciding factor, a USB interface with Linux support. Fortunately the excellent <a href="http://code.google.com/p/pywws/">PyWWS</a> supports a range of weather stations, including the one I brought.n
I'm not going to go into how I <a href="http://www.flickr.com/photos/andrew_j_w/6246463884/">mounted the system</a>, or configured PyWWS. That's all covered in the documentation. PyWWS can produce a static website, but as someone who earns his living building websites I wanted something a bit better. <a href="http://wp.me/pkxET-6z">Continuing</a> my experiments with CouchDB I decided to build the website as a <a href="http://couchapp.org/">CouchApp</a>.n
As well as allowing you to query your data with Javascript, CouchDB lets you display webpages directly out of your database. If you visit <a href="http://www.welwynweather.co.uk">welwynweather.co.uk</a> you'll notice that you're redirected to a url that contains url arguments that look a lot like those used to <a href="http://wiki.apache.org/couchdb/HTTP_view_API#Access.2BAC8-Query">query a view</a>. That's because that's exactly what's going on. Things become clearer when you discover that that <a href="http://www.welwynweather.co.uk">http://www.welwynweather.co.uk</a> is an alias for <a href="http://db.welwynweather.co.uk/_design/weather/_rewrite/">http://db.welwynweather.co.uk/_design/weather/_rewrite/</a>. Now you can see a more complete CouchDB URL, albeit without the database name. <a href="http://db.welwynweather.co.uk/">db.welwynweather.co.uk</a> points to an Apache reverse proxy that routes requests through to CouchDB.n
Over the next few posts I'll detail how the CouchApp works, but to get started you can clone my app and poke it yourself. Once you've installed the <tt>couchapp</tt> command line client simply run <tt>couchapp clone http://db.welwynweather.co.uk/_design/weather</tt>. This will give you a directory, <tt>weather</tt>, that contains a number of subdirectories including <tt>templates</tt> and <tt>views</tt> which contain the complete website.n
To deploy the site to your own server you need to create a database and then run <tt>couchapp push weather http://localhost:5984/welwynweather</tt>. Visiting <tt>http://localhost:5984/welwynweather/_design/weather/_rewrite/</tt> should show you the site. You'll need some data though, and you can use CouchDB replication to pull my data to your server. Using Futon simply set <tt>http://db.welwynweather.co.uk/</tt> as the replication source and your database as the destination and you'll quickly get a complete copy of the database.n
When replicating my data you currently cannot use continuous replication. When it completes replication CouchDB calls <tt>POST /_ensure_full_commit</tt>, but obviously I've disabled <tt>POST</tt>, <tt>PUT</tt> and <tt>DELETE</tt> on my server. This causes replication to fail and to restart from the beginning. The data will already have been copied, but CouchDB will copy it again. If you have any ideas on how to avoid this, please answer my <a href="http://stackoverflow.com/q/8309521/2990">StackOverflow question</a>.n
The website consists of four main pages. When you visit you are redirected to a page that shows the weather for the current day. Clicking on the date at the top of the page lets you also view the weather by month and by year. The daily weather pages show as much detail as is recorded by the station, in my case this is an update every five minutes. The monthly page is much the same except that the values are averaged across an hour. The yearly page is a bit different as it shows a single point for each day. An average temperature for each day is not that useful so we calculate the high and low for each day and display that.n
The final page is the records page. This displays information like the highest and lowest temperature ever recorded and the heaviest rain by hour and by day. The previous three pages are all fully generated by the server. The records page is a bit different though as calculating the records in one step is a bit complicated, instead we use AJAX to load each record individually. This means we can focus on each record keeping the code simple.n
In the next post I'll discuss how I import data into CouchDB and the basics of rendering a page in a CouchApp.n
<hr />
If you visit the site you may find that there is no recent weather data. This is because I run PyWWS on my <a href="http://www.mythtv.org">MythTV</a> box. Rather than running the PC all the time the weather data only updates when a programme is being recorded, or I'm watching TV.n
<hr />
Photo of <a href="http://www.flickr.com/photos/aigle_dore/4650548165/">Rain</a> by <a href="http://www.flickr.com/photos/aigle_dore/">Moyan Brenn</a>.n
