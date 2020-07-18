---
layout: post
title: Scalable Collaborative Filtering With MongoDB
date: 2012-03-28 13:46:04.000000000 +01:00
type: post
parent_id: '0'
published: true
password: ''
status: publish
categories:
- web development
tags:
- collaborative filtering
- mapreduce
- mongodb
- python
- similarity
meta:
  _edit_last: '364050'
  publicize_results: a:1:{s:7:"twitter";a:1:{i:5934552;a:2:{s:7:"user_id";s:10:"andrew_j_w";s:7:"post_id";s:18:"184984708529143808";}}}
  _wpas_done_twitter: '1'
  twitter_cards_summary_img_size: a:7:{i:0;i:240;i:1;i:160;i:2;i:2;i:3;s:24:"width="240"
    height="160"";s:4:"bits";i:8;s:8:"channels";i:3;s:4:"mime";s:10:"image/jpeg";}
author:
  login: andrewjw
  email: andrewjwilkinson@gmail.com
  display_name: Andrew Wilkinson
  first_name: Andrew
  last_name: Wilkinson
permalink: "/2012/03/28/scalable-collaborative-filtering-with-mongodb/"
---
<a href="http://www.flickr.com/photos/emiline220/4340980647/"><img style="float:right;border:0;" src="{{ site.baseurl }}/assets/4340980647_3436e703ed_m.jpg" alt="Book Addiction" /></a>Many websites have some form of recommendation system. While it's simple to create a recommendation system for small amounts of data, how do you create a system that scales to huge amounts of data? n
How to actually calculate the similarity of two items is a complicated topic with many possible solutions. Which one if appropriate depends on your particularly application. If you want to find out more I suggest reading the excellent <a href="http://www.amazon.co.uk/gp/product/0596529325/ref=as_li_ss_tl?ie=UTF8&amp;tag=indiegicouk-21&amp;linkCode=as2&amp;camp=1634&amp;creative=19450&amp;creativeASIN=0596529325">Programming Collective Intelligence</a><img src="{{ site.baseurl }}/assets/ir?t=indiegicouk-21&amp;l=as2&amp;o=2&amp;a=0596529325" width="1" height="1" border="0" alt="" style="border:none!important;margin:0!important;" /> (Amazon affiliate link) by Toby Segaran.n
We'll take the simplest method for calculating similarity and just calculate the percentage of users who have visited both pages compared to the total number who have visited either. If we have Page 1 that was visited by user A, B and C and Page 2 that was visited by A, C and D then the A and C visited both, but A, B, C and D visited either one so the similarity is 50%.n
With thousands or millions of items and millions or billions of views calculating the similarity between items becomes a difficult problem. Fortunately MongoDB's sharding and replication allow us to scale the calculations to cope with these large datasets.n
First let's create a set of views across a number of items. A view is stored as a single document in MongoDB. You would probably want to include extra information such as the time of the view, but for our purposes this is all that is required.n
[code language="python"]<br />
views = [<br />
        { &quot;user&quot;: &quot;0&quot;, &quot;item&quot;: &quot;0&quot; },<br />
        { &quot;user&quot;: &quot;1&quot;, &quot;item&quot;: &quot;0&quot; },<br />
        { &quot;user&quot;: &quot;1&quot;, &quot;item&quot;: &quot;0&quot; },<br />
        { &quot;user&quot;: &quot;1&quot;, &quot;item&quot;: &quot;1&quot; },<br />
        { &quot;user&quot;: &quot;2&quot;, &quot;item&quot;: &quot;0&quot; },<br />
        { &quot;user&quot;: &quot;2&quot;, &quot;item&quot;: &quot;1&quot; },<br />
        { &quot;user&quot;: &quot;2&quot;, &quot;item&quot;: &quot;1&quot; },<br />
        { &quot;user&quot;: &quot;3&quot;, &quot;item&quot;: &quot;1&quot; },<br />
        { &quot;user&quot;: &quot;3&quot;, &quot;item&quot;: &quot;2&quot; },<br />
        { &quot;user&quot;: &quot;4&quot;, &quot;item&quot;: &quot;2&quot; },<br />
    ]n
for view in views:<br />
    db.views.insert(view)<br />
[/code]n
The first step is to process this list of view of events so we can take a single item and get a list of all the users that have viewed it. To make sure this scales over a large number of views we'll use <a href="http://www.mongodb.org/display/DOCS/MapReduce">MongoDB's map/reduce</a> functionality.n
[code language="python"]<br />
def article_user_view_count():<br />
    map_func = &quot;&quot;&quot;<br />
function () {<br />
    var view = {}<br />
    view[this.user] = 1<br />
    emit(this.item, view);<br />
}<br />
&quot;&quot;&quot;<br />
[/code]n
We'll build a javascript Object where the keys are the user id and the value is the number of time that user has viewed this item. In the map function we we build an object that represents a single view and <tt>emit</tt> it using the item id as the key. MongoDB will group all the objects emitted with the same key and run the reduce function, shown below.n
[code language="python"]<br />
    reduce_func = &quot;&quot;&quot;<br />
function (key, values) {<br />
    var view = values[0];n
    for (var i = 1; i &lt; values.length; i++) {<br />
        for(var item in values[i]) {<br />
            if(!view.hasOwnProperty(item)) { view[item] = 0; }n
            view[item] = view[item] + values[i][item];<br />
        }<br />
    }<br />
    return view;<br />
}<br />
&quot;&quot;&quot;<br />
[/code]n
A reduce function takes two parameters, the key and a list of values. The values that are passed in can either be those <tt>emit</tt>ted by the map function, or values returned from the <tt>reduce</tt> function. To help it scale not all of the original values will be processed at once, and the reduce function must be able to handle input from the map function or its own output. Here we output a value in the same format as the input so we don't need to do anything special.n
[code language="python"]<br />
    db.views.map_reduce(Code(map_func), Code(reduce_func), out=&quot;item_user_view_count&quot;)<br />
[/code]n
The final step is to run the functions we've just created and output the data into a new collection. Here we're recalculating all the data each time this function is run. To scale properly you should filter the input based on the date the view occurred and merge it with the output collection, rather than replacing it as we are doing here.n
Now we need calculate a matrix of similarity values, linking each item with every other item. First lets see how we can calculate the similarity of all items to one single item. Again we'll use map/reduce to help spread the load of running this calculation. Here we'll just use the map part of map/reduce because each input document will be represented by a single output document.n
[code language="python"]<br />
def similarity(item):<br />
    map_func = &quot;&quot;&quot;<br />
function () {<br />
    if(this._id == &quot;%s&quot;) { return; }n
    var viewed_both = {};<br />
    var viewed_any = %s;n
    for (var user in this.views) {<br />
        if(this.value.hasOwnProperty(user)) {<br />
            viewed_both[user] = 1;<br />
        }n
        viewed_any[user] = 1;<br />
     }n
     emit(&quot;%s&quot;+&quot;_&quot;+this._id, viewed_both.length / viewed_any.length );<br />
}<br />
&quot;&quot;&quot; % (int(item[&quot;_id&quot;]), json.dumps(item[&quot;value&quot;]), json.dumps(item[&quot;value&quot;]) int(item[&quot;_id&quot;]), )<br />
[/code]n
The input to our Python function is a document that was outputted by our previous map/reduce call. We build a new Javascript by interpolating some data from this document into a template function. We loop through all the users who viewed the document we're comparing against and work out whether they have viewed both. At the end of the function we emit the percentage of users who viewed both.n
[code language="python"]<br />
    reduce_func = &quot;&quot;&quot;<br />
function (key, values) {<br />
    return results[0];<br />
}<br />
&quot;&quot;&quot;<br />
[/code]n
    Because we output unique ids in the map function this reduce function will only be called with a single value so we just return that.n
[code language="python"]<br />
    db.item_user_view_count.map_reduce(Code(map_func), Code(reduce_func), out=SON([(&quot;merge&quot;, &quot;item_similarity&quot;)]))<br />
[/code]n
The last step in this function is to run the map reduce. Here as we're running the map/reduce multiple times we need to merge the output rather than replacing it as we did before.n
The final step is to loop through the output from our first map/reduce and call our second function for each item.n
[code language="python"]<br />
for doc in db.item_user_view_count.find():<br />
    similarity(doc)<br />
[/code]n
A key thing to realise is that you don't need to calculate live similarity data. Once you have even a few hundred views per item then the similarity will remain fairly consistent. In this example we step through each item in turn and calculate the similarity for it with every other item. For a million item database where each iteration of this loop takes one second the similarity data will be updated once every 11 days. n
I'm not claiming that you can take the code provided here and immediately have a massively scalable system. MongoDB provides an easy to use replication and sharding system, which are plugged in to its Map/Reduce framework. What you should take away is that by using map/reduce with sharding and replication to calculate the similarity between two items we can quickly get a system that scales well with an increasing number of items and of views.n
<hr />
Photo of <a href="http://www.flickr.com/photos/emiline220/4340980647/">Book Addiction</a> by <a href="http://www.flickr.com/photos/emiline220/">Emily Carlin</a>.n