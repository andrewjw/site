---
layout: post
title: Beating Google With CouchDB, Celery and Whoosh (Part 3)
date: 2011-10-04 12:00:18.000000000 +01:00
tags:
- web development
- celery
- celerycrawler
- couchdb
- django
permalink: "/2011/10/04/beating-google-with-couchdb-celery-and-whoosh-part-3/"
flickr_user: 'https://www.flickr.com/photos/tim_ellis/'
flickr_username: "Tim Ellis"
flickr_image: 'https://live.staticflickr.com/5269/5586571637_f106791f3b_w.jpg'
flickr_imagelink: 'https://www.flickr.com/photos/tim_ellis/5586571637/'
flickr_imagename: 'Celery'
---
In this series I'll show you how to build a search engine using standard Python tools like Django, Whoosh and
CouchDB. In this post we'll start crawling the web and filling our database with the contents of pages.

One of the rules we set down was to not request a page too often. If, by accident, we try to retrieve a page
more than once a week then don't want that request to actually make it to the internet. To help prevent this
we'll extend the `Page` class we created in the last post with a function called `get_by_url`.
This static method will take a url and return the Page object that represents it, retrieving the page if we
don't already have a copy. You could create this as an independent function, but I prefer to use static
methods to keep things tidy.

We only actually want to retrieve the page from the internet in one of the three tasks the we're going to
create so we'll give `get_by_url` a parameter, `update` that enables us to return `None`
if we don't have a copy of the page.

```python
@staticmethod
def get_by_url(url, update=True):
    r = settings.db.view("page/by_url", key=url)
    if len(r.rows) == 1:
        doc = Page.load(settings.db, r.rows[0].value)
        if doc.is_valid():
            return doc
    elif not update:
        return None
    else:
        doc = Page(url=url)
        doc.update()
        return doc
```

The key line in the static method is `doc.update()`. This calls the function to retrieves the page and
makes sure we respect the `robots.txt` file. Let's look at what happens in that function.
<!--more-->

```python
def update(self):
    parse = urlparse(self.url)
```

We need to split up the given URL so we know whether it's a secure connection or not, and we need to limit our
connects to each domain so we need get that as well. Python has a module,
[urlparse](http://docs.python.org/library/urlparse.html), that does the hard work for us.

```python
    robotstxt = RobotsTxt.get_by_domain(parse.scheme, parse.netloc)
    if not robotstxt.is_allowed(parse.netloc):
        return False
```

In the previous post we discussed parsing the `robots.txt` file and here we make sure that if we're not
allowed to index a page, then we don't

```python
    while cache.get(parse.netloc)
        is not None:
            time.sleep(1)
            cache.set(parse.netloc, True, 10)
```

As with the code to parse `robots.txt` files we need to make sure we don't access the same domain too
often.

```python
    req = Request(self.url, None, { "User-Agent": settings.USER_AGENT })
    resp = urlopen(req)
    if not resp.info()["Content-Type"].startswith("text/html"):
        return
    self.content = resp.read().decode("utf8")
    self.last_checked = datetime.now()
    self.store(settings.db)
```

Finally, once we've checked we're allowed to access a page and haven't accessed another page on the same
domain recently we use the standard Python tools to download the content of the page and store it in our
database.n Now we can retrieve a page we need to add it to the task processing system. To do this we'll create
a [Celery](http://celeryproject.org/) task to retrieve the page. The task just needs to call the
`get_by_url` static method we created earlier and then, if the page is downloaded trigger a second task
to parse out all of the links.

```python
@task
def retrieve_page(url):
    page = Page.get_by_url(url)
    if page is None:
        return
    find_links.delay(page.id)
```

You might be asking why the links aren't parsed immediately after retrieving the page. They certainly could
be, but a key goal was to enable the crawling process to scale as much as possible. Each page crawled has,
based on the pages I've crawled so far, around 100 links on it. As part of the `find_links` task a new
`retrieve_task` is created. This quickly swamps the tasks to perform other tasks like calculating the
rank of a page and prevents them from being processed.

Celery provides the tools to ensure that a subset of message are processed in a timely manner, called
`Queues`. Tasks can be assigned to different queues and daemons can be made to watch a specific set of
queues. If you have a Celery daemon that only watches the queue used by your high priority tasks then those
tasks will always be processed quickly.

We'll use two queues, one for retrieving the pages and another for processing them. First we need to tell
Celery about the queues (we also need to include the default `celery` queue here) and then we create a
router class. The router looks at the task name and decides which queue to put it into. Your routing code
could be very complicated, but ours is very straightforward.

```python
CELERY_QUEUES = {
    "retrieve": {
        "exchange": "default",
        "exchange_type": "direct",
        "routing_key": "retrieve"
    },
    "process": {
        "exchange": "default",
        "exchange_type": "direct",
        "routing_key": "process "
    },
    "celery": {
        "exchange": "default",
        "exchange_type": "direct",
        "routing_key": "celery"
    }
}

class MyRouter(object):
    def route_for_task(self, task, args=None, kwargs=None):
        if task == "crawler.tasks.retrieve_page":
            return { "queue": "retrieve" }
        else:
            return { "queue": "process" }

CELERY_ROUTES = (MyRouter(), )
```

The final step is to allow the crawler to be kicked off by seeding it with some URLs. I've previously posted
about how to create a
[Django management
command](/2009/03/06/creating-django-management-commands/) and they're a perfect fit here. The command takes one argument, the url, and creates a Celery task
to retrieve it.

```python
class Command(BaseCommand):
    def handle(self, url, **options):
        retrieve_page.delay(url)
```

We've now got a web crawler that is almost complete. In the next post I'll discuss parsing links out of the
HTML, and we'll look at calculating the rank of each page.

Read [part 4](/2011/10/06/beating-google-with-couchdb-celery-and-whoosh-part-4/).
