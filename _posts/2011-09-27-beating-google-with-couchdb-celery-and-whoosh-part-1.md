---
layout: post
title: Beating Google With CouchDB, Celery and Whoosh (Part 1)
date: 2011-09-27 12:00:44.000000000 +01:00
type: post
parent_id: '0'
published: true
password: ''
status: publish
categories:
- web development
tags: celery celerycrawler couchdb django python whoosh
meta:
  _edit_last: '364050'
  _wpas_done_twitter: '1'
  twitter_cards_summary_img_size: a:7:{i:0;i:240;i:1;i:180;i:2;i:2;i:3;s:24:"width="240"
    height="180"";s:4:"bits";i:8;s:8:"channels";i:3;s:4:"mime";s:10:"image/jpeg";}
author:
  login: andrewjw
  email: andrewjwilkinson@gmail.com
  display_name: Andrew Wilkinson
  first_name: Andrew
  last_name: Wilkinson
permalink: "/2011/09/27/beating-google-with-couchdb-celery-and-whoosh-part-1/"
---
<a href="http://www.flickr.com/photos/judy-van-der-velden/5668310473/"><img src="{{ site.baseurl }}/assets/5668310473_1573cde550_m.jpg" alt="celery by Judy **" style="float:right;border:0;" /></a>Ok, let's get this out of the way right at the start - the title is a huge overstatement. This series of posts will show you how to create a search engine using standard Python tools like Django, Celery and Whoosh with CouchDB as the backend.n
<a href="http://celeryproject.org/">Celery</a> is a message passing library that makes it really easy to run background tasks and to spread them across a number of nodes. The most recent release added the NoSQL database <a href="http://couchdb.apache.org/">CouchDB</a> as a possible backend. I'm a huge fan of CouchDB, and the idea of running both my database and message passing backend on the same software really appealed to me. Unfortunately the documentation doesn't make it clear what you need to do to get CouchDB working, and what the downsides are. I decided to write this series partly to explain how Celery and CouchDB work, but also to experiment with using them together.n
In this series I'm going to talk about setting up Celery to work with Django, using CouchDB as a backend. I'm also going to show you how to use Celery to create a web-crawler. We'll then index the crawled pages using <a href="https://bitbucket.org/mchaput/whoosh/wiki/Home">Whoosh</a> and use a <a href="http://en.wikipedia.org/wiki/PageRank">PageRank</a>-like algorithm to help rank the results. Finally, we'll attach a simple Django frontend to the search engine for querying it.n
Let's consider what we need to implement for our webcrawler to work, and be a good citizen of the internet. First and foremost is that we must be read and respect <a href="http://www.robotstxt.org/">robots.txt</a>. This is a file that specifies what areas of a site crawlers are banned from. We must also not hit a site too hard, or too often. It is very easy to write a crawler than repeatedly hits a site, and requests the same document over and over again. These are very big no-noes. Lastly we must make sure that we use a custom <a href="http://en.wikipedia.org/wiki/User_agent">User Agent</a> so our bot is identifiable.n
We'll divide the algorithm for our webcrawler into three parts. Firstly we'll need a set of urls. The crawler picks a url, retrieves the page then store it in the database. The second stage takes the page content, parses it for links, and adds the links to the set of urls to be crawled. The final stage is to index the retrieved text. This is done by watching for pages that are retrieved by the first stage, and adding them to the full text index.n
Celery's allows you to create 'tasks'. These are units of work that are triggered by a piece of code and then executed, after a period of time, on any node in your system. For the crawler we'll need two seperate tasks. The first retrieves and stores a given url. When it completes it will triggers a second task, one that parses the links from the page. To begin the process we'll need to use an external command to feed some initial urls into the system, but after that it will continuously crawl until it runs out of links. A real search engine would want to monitor its index for stale pages and reload those, but I won't implement that in this example.n
I'm going to assume that you have a decent level of knowledge about <a href="http://www.python.org">Python</a> and <a href="http://www.djangoproject.com/">Django</a>, so you might want to read some tutorials on those first. If you're following along at home, create yourself a blank Django project with a single app inside. You'll also need to install <tt>django-celery</tt>, the CouchDB Python library, and have a working install of CouchDB available.n
Read <a href="http://wp.me/pkxET-6E">part 2</a>.n
<hr />
Photo of <a href="http://www.flickr.com/photos/judy-van-der-velden/5668310473/">celery</a> by <a href="http://www.flickr.com/photos/judy-van-der-velden/">Judy **</a>.n