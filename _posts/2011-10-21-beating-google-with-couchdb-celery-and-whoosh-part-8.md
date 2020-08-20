---
layout: post
title: Beating Google With CouchDB, Celery and Whoosh (Part 8)
date: 2011-10-21 12:00:18.000000000 +01:00
type: post
tags:
- web development
- celery
- celerycrawler
- couchdb
- django
permalink: "/2011/10/21/beating-google-with-couchdb-celery-and-whoosh-part-8/"
flickr_user: 'https://www.flickr.com/photos/othree/'
flickr_username: "othree"
flickr_image: 'https://live.staticflickr.com/5245/5228608281_2d50d3855c_w.jpg'
flickr_imagelink: 'https://www.flickr.com/photos/othree/5228608281/'
flickr_imagename: 'github 章魚貼紙'
---
In the previous seven posts I've gone through all the stages in building a search engine. If you want to try
and run it for yourself and tweak it to make it even better then you can. I've put the <a
href="https://github.com/andrewjw/celery-crawler">code up on GitHub</a>. All I ask is that if you beat Google,
you give me a credit somewhere.

When you've downloaded the code it should prove to be quite simple to get running. First you'll need to edit
settings.py. It should work out of the box, but you should change the `USER_AGENT` setting to something
unique. You may also want to adjust some of the other settings, such as the database connection or CouchDB
urls.n To set up the CouchDB views type `python manage.py update_couchdb`.

Next, to run the celery daemon you'll need to type the following two commands:
```bash
python manage.py celeryd -Q retrieve
python manage.py celeryd -Q process
```

 This sets up the daemons to monitor the two queues and process the tasks. As mentioned in a previous post
two queues are needed to prevent one set of tasks from swamping the other.

Next you'll need to run the full text indexer, which can be done with `python manage.py index_update`
and then you'll want to run the server using `python manage.py runserver`.

At this point you should have several process running not doing anything. To kick things off we need to inject
one or more urls into the system. You can do this with another management command, `python manage.py
start_crawl http://url`. You can run this command as many times as you like to seed your crawler with
different pages. It has been my experience that the average page has around 100 links on it so it shouldn't
take long before your crawler is scampering off to crawl many more pages that you initially seeded it with.

So, how well does Celery work with CouchDB as a backend? The answer is that it's a bit mixed. Certainly it
makes it very easy to get started as you can just point it at the server and it just works. However, the
drawback, and it's a real show stopper, is that the Celery daemon will poll the database looking for new
tasks. This polling, as you scale up the number of daemons will quickly bring your server to its knees and
prevent it from doing any useful work.

The disappointing fact is that Celery could watch the `_changes` feed rather than polling. Hopefully
this will get fixed in a future version. For now though, for anything other experimental scale installations
RabbitMQ is a much better bet.

Hopefully this series has been useful to you, and please do download the code and experiment with it!
