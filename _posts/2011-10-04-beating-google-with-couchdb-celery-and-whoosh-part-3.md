---
layout: post
title: Beating Google With CouchDB, Celery and Whoosh (Part 3)
date: 2011-10-04 12:00:18.000000000 +01:00
type: post
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
we'll extend the <tt>Page</tt> class we created in the last post with a function called <tt>get_by_url</tt>.
This static method will take a url and return the Page object that represents it, retrieving the page if we
don't already have a copy. You could create this as an independent function, but I prefer to use static
methods to keep things tidy.

We only actually want to retrieve the page from the internet in one of the three tasks the we're going to
create so we'll give <tt>get_by_url</tt> a parameter, <tt>update</tt> that enables us to return <tt>None</tt>
if we don't have a copy of the page.

{% highlight python %}
@staticmethod
def get_by_url(url, update=True):
    r = settings.db.view(&quot;page/by_url&quot;, key=url)
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
{% endhighlight %}

The key line in the static method is <tt>doc.update()</tt>. This calls the function to retrieves the page and
makes sure we respect the <tt>robots.txt</tt> file. Let's look at what happens in that function

{% highlight python %}
def update(self):
    parse = urlparse(self.url)
{% endhighlight %}

We need to split up the given URL so we know whether it's a secure connection or not, and we need to limit our
connects to each domain so we need get that as well. Python has a module, <a
href="http://docs.python.org/library/urlparse.html">urlparse</a>, that does the hard work for us.

{% highlight python %}
    robotstxt = RobotsTxt.get_by_domain(parse.scheme, parse.netloc)
    if not robotstxt.is_allowed(parse.netloc):
        return False
{% endhightlight %}

In the previous post we discussed parsing the <tt>robots.txt</tt> file and here we make sure that if we're not
allowed to index a page, then we don't

{% highlight python %}
    while cache.get(parse.netloc)
        is not None:
            time.sleep(1)
            cache.set(parse.netloc, True, 10)
{% endhightlight %}

As with the code to parse <tt>robots.txt</tt> files we need to make sure we don't access the same domain too
often.

{% highlight python %}
    req = Request(self.url, None, { &quot;User-Agent&quot;: settings.USER_AGENT })
    resp = urlopen(req)
    if not resp.info()[&quot;Content-Type&quot;].startswith(&quot;text/html&quot;):
        return
    self.content = resp.read().decode(&quot;utf8&quot;)
    self.last_checked = datetime.now()
    self.store(settings.db)
{% endhightlight %}

Finally, once we've checked we're allowed to access a page and haven't accessed another page on the same
domain recently we use the standard Python tools to download the content of the page and store it in our
database.n Now we can retrieve a page we need to add it to the task processing system. To do this we'll create
a <a href="http://celeryproject.org/">Celery</a> task to retrieve the page. The task just needs to call the
<tt>get_by_url</tt> static method we created earlier and then, if the page is downloaded trigger a second task
to parse out all of the links.

{% highlight python %}
@task
def retrieve_page(url):
    page = Page.get_by_url(url)
    if page is None:
        return
    find_links.delay(page.id)
{% endhightlight %}

You might be asking why the links aren't parsed immediately after retrieving the page. They certainly could
be, but a key goal was to enable the crawling process to scale as much as possible. Each page crawled has,
based on the pages I've crawled so far, around 100 links on it. As part of the <tt>find_links</tt> task a new
<tt>retrieve_task</tt> is created. This quickly swamps the tasks to perform other tasks like calculating the
rank of a page and prevents them from being processed.

Celery provides the tools to ensure that a subset of message are processed in a timely manner, called
<tt>Queues</tt>. Tasks can be assigned to different queues and daemons can be made to watch a specific set of
queues. If you have a Celery daemon that only watches the queue used by your high priority tasks then those
tasks will always be processed quickly.

We'll use two queues, one for retrieving the pages and another for processing them. First we need to tell
Celery about the queues (we also need to include the default <tt>celery</tt> queue here) and then we create a
router class. The router looks at the task name and decides which queue to put it into. Your routing code
could be very complicated, but ours is very straightforward.

{% highlight python %}
CELERY_QUEUES = {
    &quot;retrieve&quot;: {
        &quot;exchange&quot;: &quot;default&quot;,
        &quot;exchange_type&quot;: &quot;direct&quot;,
        &quot;routing_key&quot;: &quot;retrieve&quot;
    },
    &quot;process&quot;: {
        &quot;exchange&quot;: &quot;default&quot;,
        &quot;exchange_type&quot;: &quot;direct&quot;,
        &quot;routing_key&quot;: &quot;process &quot;
    },
    &quot;celery&quot;: {
        &quot;exchange&quot;: &quot;default&quot;,
        &quot;exchange_type&quot;: &quot;direct&quot;,
        &quot;routing_key&quot;: &quot;celery&quot;
    }
}

class MyRouter(object):
    def route_for_task(self, task, args=None, kwargs=None):
        if task == &quot;crawler.tasks.retrieve_page&quot;:
            return { &quot;queue&quot;: &quot;retrieve&quot; }
        else:
            return { &quot;queue&quot;: &quot;process&quot; }

CELERY_ROUTES = (MyRouter(), )
{% endhightlight %}

The final step is to allow the crawler to be kicked off by seeding it with some URLs. I've previously posted
about how to create a <a
href="http://andrewwilkinson.wordpress.com/2009/03/06/creating-django-management-commands/">Django management
command</a> and they're a perfect fit here. The command takes one argument, the url, and creates a Celery task
to retrieve it.

{% highlight python %}
class Command(BaseCommand):
    def handle(self, url, **options):
        retrieve_page.delay(url)
{% endhightlight %}

We've now got a web crawler that is almost complete. In the next post I'll discuss parsing links out of the
HTML, and we'll look at calculating the rank of each page.

Read <a href="/2011/10/06/beating-google-with-couchdb-celery-and-whoosh-part-4/">part 4</a>.
