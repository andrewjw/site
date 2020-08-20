---
layout: post
title: Beating Google With CouchDB, Celery and Whoosh (Part 7)
date: 2011-10-19 12:00:16.000000000 +01:00
type: post
tags:
- celery
- celerycrawler
- couchdb
- django
- web development
permalink: "/2011/10/19/beating-google-with-couchdb-celery-and-whoosh-part-7/"
flickr_user: 'https://www.flickr.com/photos/small_realm/'
flickr_username: "Bob Mical"
flickr_image: 'https://live.staticflickr.com/5483/11189803153_2a7421916d_w.jpg'
flickr_imagelink: 'https://www.flickr.com/photos/small_realm/11189803153/'
flickr_imagename: 'Data Center'
---
The key ingredients of our search engine are now in place, but we face a problem. We can download webpages and
store them in [CouchDB](http://couchdb.apache.org/). We can rank them in order of importance and
query them using [Whoosh](https://bitbucket.org/mchaput/whoosh/wiki/Home) but the internet is big,
[really big!](http://thenextweb.com/shareables/2011/01/11/infographic-how-big-is-the-internet/) A
single server doesn't even come close to being able to hold all the information that you would want it to -
Google has an estimated 
[900,000
servers](http://www.datacenterknowledge.com/archives/2009/05/14/whos-got-the-most-web-servers/). So how do we scale this the software we've written so far effectively?

The reason I started writing this series was to investigate how well Celery's integration with CouchDB works.
This gives us an immediate win in terms of scaling as we don't need to worry about a different backend, such
as [RabbitMQ](http://www.rabbitmq.com/). Celery itself is designed to scale so we can run
`celeryd` daemons as many boxes as we like and the jobs will be divided amongst them. This means that
our indexing and ranking processes will scale easily.

CouchDB is not designed to scale across multiple machines, but there is some mature software, 
[CouchDB-lounge](http://tilgovi.github.com/couchdb-lounge/) that does just that. I won't go into how
to get set this up but fundamentally you set up a proxy that sits in front of your CouchDB cluster and shards
the data across the nodes. It deals with the job of merging view results and managing where the data is
actually stored so you don't have to. O'Reilly's CouchDB: The Definitive Guide has a chapter 
[on clustering](http://guide.couchdb.org/draft/clustering.html) that is well worth a read.

Unfortunately while Woosh is easy to work with it's not designed to be used on a large scale. Indeed if
someone was crazy enough to try to run the software we've developed in this series they might be advised to
replace Whoosh with [Solr](http://lucene.apache.org/solr/). Solr is a lucene-based search server
which provides an HTTP interface to the full-text index. Solr comes with a 
[sharding system](http://wiki.apache.org/solr/DistributedSearch) to enable you to query an index that
is too large for a single machine.

So, with our two data storage tools providing HTTP interface and both having replication and sharding either
built in or as available as a proxy the chances of being able to scale effectively are good. Celery should
allow the background tasks that are needed to run a search engine can be scaled, but the challenges of
building and running a large scale infrastructure are many and I would not claim that these tools mean success
is guarenteed!n In the final post of this series I will discuss what I've learnt about running Celery with
CouchDB, and with CouchDB in general. I'll also describe how to download and run the complete code so you can
try these techniques for yourself.

Read [part 8](/2011/10/21/beating-google-with-couchdb-celery-and-whoosh-part-8/).
