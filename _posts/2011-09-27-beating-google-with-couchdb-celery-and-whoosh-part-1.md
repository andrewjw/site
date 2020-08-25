---
layout: post
title: Beating Google With CouchDB, Celery and Whoosh (Part 1)
date: 2011-09-27 12:00:44.000000000 +01:00
tags:
    - celery
    - celerycrawler
    - couchdb
    - django
    - python
    - web development
permalink: "/2011/09/27/beating-google-with-couchdb-celery-and-whoosh-part-1/"
flickr_user: 'https://www.flickr.com/photos/judy-van-der-velden/'
flickr_username: "Judy van der Velden"
flickr_image: 'https://live.staticflickr.com/5227/5668310473_1573cde550_w.jpg'
flickr_imagelink: 'https://www.flickr.com/photos/judy-van-der-velden/5668310473/'
flickr_imagename: 'celery'
---
Ok, let's get this out of the way right at the start - the title is a huge overstatement. This series of posts
will show you how to create a search engine using standard Python tools like Django, Celery and Whoosh with
CouchDB as the backend.

[Celery](http://celeryproject.org/) is a message passing library that makes it really easy to run
background tasks and to spread them across a number of nodes. The most recent release added the NoSQL database
[CouchDB](http://couchdb.apache.org/) as a possible backend. I'm a huge fan of CouchDB, and the
idea of running both my database and message passing backend on the same software really appealed to me.
Unfortunately the documentation doesn't make it clear what you need to do to get CouchDB working, and what the
downsides are. I decided to write this series partly to explain how Celery and CouchDB work, but also to
experiment with using them together.

In this series I'm going to talk about setting up Celery to work with Django, using CouchDB as a backend. I'm
also going to show you how to use Celery to create a web-crawler. We'll then index the crawled pages using
[Whoosh](https://bitbucket.org/mchaput/whoosh/wiki/Home) and use a
[PageRank](http://en.wikipedia.org/wiki/PageRank)-like algorithm to help rank the results. Finally,
we'll attach a simple Django frontend to the search engine for querying it.

Let's consider what we need to implement for our webcrawler to work, and be a good citizen of the internet.
First and foremost is that we must be read and respect [robots.txt](http://www.robotstxt.org/).
This is a file that specifies what areas of a site crawlers are banned from. We must also not hit a site too
hard, or too often. It is very easy to write a crawler than repeatedly hits a site, and requests the same
document over and over again. These are very big no-noes. Lastly we must make sure that we use a custom
[User Agent](http://en.wikipedia.org/wiki/User_agent) so our bot is identifiable.

We'll divide the algorithm for our webcrawler into three parts. Firstly we'll need a set of urls. The crawler
picks a url, retrieves the page then store it in the database. The second stage takes the page content, parses
it for links, and adds the links to the set of urls to be crawled. The final stage is to index the retrieved
text. This is done by watching for pages that are retrieved by the first stage, and adding them to the full
text index.

Celery's allows you to create 'tasks'. These are units of work that are triggered by a piece of code and then
executed, after a period of time, on any node in your system. For the crawler we'll need two seperate tasks.
The first retrieves and stores a given url. When it completes it will triggers a second task, one that parses
the links from the page. To begin the process we'll need to use an external command to feed some initial urls
into the system, but after that it will continuously crawl until it runs out of links. A real search engine
would want to monitor its index for stale pages and reload those, but I won't implement that in this example.

I'm going to assume that you have a decent level of knowledge about [Python](http://www.python.org)
and [Django](http://www.djangoproject.com/), so you might want to read some tutorials on those
first. If you're following along at home, create yourself a blank Django project with a single app inside.
You'll also need to install `django-celery`, the CouchDB Python library, and have a working install of
CouchDB available.

Read [part 2](/2011/09/29/beating-google-with-couchdb-celery-and-whoosh-part-2/).
