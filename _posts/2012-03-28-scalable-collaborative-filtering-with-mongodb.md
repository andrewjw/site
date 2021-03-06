---
layout: post
title: Scalable Collaborative Filtering With MongoDB
date: 2012-03-28 13:46:04.000000000 +01:00
tags:
- web development
- collaborative filtering
- mapreduce
- mongodb
- python
- similarity
permalink: "/2012/03/28/scalable-collaborative-filtering-with-mongodb/"
flickr_user: 'https://www.flickr.com/photos/emiline220/'
flickr_username: "Emily Carlin"
flickr_image: 'https://live.staticflickr.com/2728/4340980647_3436e703ed_w.jpg'
flickr_imagelink: 'https://www.flickr.com/photos/emiline220/4340980647/'
flickr_imagename: 'Book Addiction'
---
Many websites have some form of recommendation system. While it's simple to create a recommendation system for
small amounts of data, how do you create a system that scales to huge amounts of data?

How to actually calculate the similarity of two items is a complicated topic with many possible solutions.
Which one if appropriate depends on your particularly application. If you want to find out more I suggest
reading the excellent [Programming Collective Intelligence](http://www.amazon.co.uk/gp/product/0596529325/
ref=as_li_ss_tl?ie=UTF8&tag=indiegicouk-21&linkCode=as2&camp=1634&creative=19450&creativeASIN=0596529325)
(Amazon affiliate link) by Toby Segaran.

We'll take the simplest method for calculating similarity and just calculate the percentage of users who have
visited both pages compared to the total number who have visited either. If we have Page 1 that was visited by
user A, B and C and Page 2 that was visited by A, C and D then the A and C visited both, but A, B, C and D
visited either one so the similarity is 50%.
<!--more-->

With thousands or millions of items and millions or billions of views calculating the similarity between items
becomes a difficult problem. Fortunately MongoDB's sharding and replication allow us to scale the calculations
to cope with these large datasets.

First let's create a set of views across a number of items. A view is stored as a single document in MongoDB.
You would probably want to include extra information such as the time of the view, but for our purposes this
is all that is required.

```python
views = [
        { "user": "0", "item": "0" },
        { "user": "1", "item": "0" },
        { "user": "1", "item": "0" },
        { "user": "1", "item": "1" },
        { "user": "2", "item": "0" },
        { "user": "2", "item": "1" },
        { "user": "2", "item": "1" },
        { "user": "3", "item": "1" },
        { "user": "3", "item": "2" },
        { "user": "4", "item": "2" },
    ]
for view in views:
    db.views.insert(view)
```

 The first step is to process this list of view of events so we can take a single item and get a list of all
the users that have viewed it. To make sure this scales over a large number of views we'll use
[MongoDB's map/reduce](http://www.mongodb.org/display/DOCS/MapReduce) functionality.

```python
def article_user_view_count():
    map_func = """
function () {
    var view = {}
    view[this.user] = 1
    emit(this.item, view);
}
"""
```

We'll build a javascript Object where the keys are the user id and the value is the number of time that user
has viewed this item. In the map function we we build an object that represents a single view and
`emit` it using the item id as the key. MongoDB will group all the objects emitted with the same key
and run the reduce function, shown below.

```python
    reduce_func = """
function (key, values) {
    var view = values[0];
    for (var i = 1; i < values.length; i++) {
        for(var item in values[i]) {
            if(!view.hasOwnProperty(item)) { view[item] = 0; }
            view[item] = view[item] + values[i][item];
        }
    }
    return view;
}
"""
```

A reduce function takes two parameters, the key and a list of values. The values that are passed in can either
be those `emit`ted by the map function, or values returned from the `reduce` function. To help
it scale not all of the original values will be processed at once, and the reduce function must be able to
handle input from the map function or its own output. Here we output a value in the same format as the input
so we don't need to do anything special.

```python
    db.views.map_reduce(Code(map_func), Code(reduce_func), out="item_user_view_count")
```

The final step is to run the functions we've just created and output the data into a new collection. Here
we're recalculating all the data each time this function is run. To scale properly you should filter the input
based on the date the view occurred and merge it with the output collection, rather than replacing it as we
are doing here.

Now we need calculate a matrix of similarity values, linking each item with every other item. First lets see
how we can calculate the similarity of all items to one single item. Again we'll use map/reduce to help spread
the load of running this calculation. Here we'll just use the map part of map/reduce because each input
document will be represented by a single output document.

```python
def similarity(item):
    map_func = """
function () {
    if(this._id == "%s") { return; }
    var viewed_both = {};
    var viewed_any = %s;
    for (var user in this.views) {
        if(this.value.hasOwnProperty(user)) {
            viewed_both[user] = 1;
        }n
        viewed_any[user] = 1;
     }n
     emit("%s"+"_"+this._id, viewed_both.length / viewed_any.length );
}
""" % (int(item["_id"]), json.dumps(item["value"]), json.dumps(item["value"]) int(item["_id"]), )
```

The input to our Python function is a document that was outputted by our previous map/reduce call. We build a
new Javascript by interpolating some data from this document into a template function. We loop through all the
users who viewed the document we're comparing against and work out whether they have viewed both. At the end
of the function we emit the percentage of users who viewed both.

```python
    reduce_func = """
function (key, values) {
    return results[0];
}
"""
```

Because we output unique ids in the map function this reduce function will only be called with a single value so we just return that.

```python
    db.item_user_view_count.map_reduce(Code(map_func), Code(reduce_func), out=SON([("merge", "item_similarity")]))
```

The last step in this function is to run the map reduce. Here as we're running the map/reduce multiple times
we need to merge the output rather than replacing it as we did before.

The final step is to loop through the output from our first map/reduce and call our second function for each
item.

```python
for doc in db.item_user_view_count.find():
    similarity(doc)
```

 A key thing to realise is that you don't need to calculate live similarity data. Once you have even a few
hundred views per item then the similarity will remain fairly consistent. In this example we step through
each item in turn and calculate the similarity for it with every other item. For a million item database
where each iteration of this loop takes one second the similarity data will be updated once every 11 days.

I'm not claiming that you can take the code provided here and immediately have a massively scalable system.
MongoDB provides an easy to use replication and sharding system, which are plugged in to its Map/Reduce
framework. What you should take away is that by using map/reduce with sharding and replication to calculate
the similarity between two items we can quickly get a system that scales well with an increasing number of
items and of views.
