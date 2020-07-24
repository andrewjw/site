---
layout: post
title: 'Beating Google With CouchDB, Celery and Whoosh (Part 2)'
date: {}
type: post
parent_id: '0'
published: true
status: publish
categories:
  - web development
tags:
  - celery
  - celerycrawler
  - couchdb
  - django
  - python
  - whoosh
meta:
  _edit_last: '364050'
  _wpas_done_twitter: '1'
author:
  login: andrewjw
  email: andrewjwilkinson@gmail.com
  display_name: Andrew Wilkinson
  first_name: Andrew
  last_name: Wilkinson
permalink: /2011/09/29/beating-google-with-couchdb-celery-and-whoosh-part-2/
---
<a href="http://www.flickr.com/photos/johnnystiletto/5226474427/"><img style="float:right;border:0;" src="{{ site.baseurl }}/assets/5226474427_90d7388bed_m.jpg" alt="Celery, Carrots &amp; Sweet Onion for Chicken Feet Stock by I Believe I Can Fry" /></a>In this <a href="http://andrewwilkinson.wordpress.com/2011/09/27/beating-google-with-couchdb-celery-and-whoosh-part-1/">series</a> I'll show you how to build a search engine using standard Python tools like Django, Whoosh and CouchDB. In this post we'll begin by creating the data structure for storing the pages in the database, and write the first parts of the webcrawler.n
CouchDB's Python library has a simple <a href="http://packages.python.org/CouchDB/mapping.html">ORM system</a> that makes it easy to convert between the JSON objects stored in the database and a Python object.

To create the class you just need to specify the names of the fields, and their type. So, what do a search engine need to store? The url is an obvious one, as is the content of the page. We also need to know when we last accessed the page. To make things easier we'll also have a list of the urls that the page links to. One of the great advantages of a database like CouchDB is that we don't need to create a separate table to hold the links, we can just include them directly in the main document. To help return the best pages we'll use a <a href="http://en.wikipedia.org/wiki/PageRank">page rank</a> like algorithm to rank the page, so we also need to store that rank. Finally, as is good practice on CouchDB we'll give the document a <tt>type</tt> field so we can write views that only target this document type.

{% highlight python %}
class Page(Document):
    type = TextField(default=&quot;page&quot;)
    url = TextField()
    content = TextField()
    links = ListField(TextField())
    rank = FloatField(default=0)
    last_checked = DateTimeField(default=datetime.now)
{% endhighlight %}

That's a lot of description for not a lot of code! Just add that class to your <tt>models.py</tt> file. It's not a normal Django model, but we're not using Django models in this project so it's the right place to put it. 

We also need to keep track of the urls that we are and aren't allowed to access. Fortunately for us Python comes with a class, <a href="http://docs.python.org/library/robotparser.html">RobotFileParser</a> which handles the parsing of the file for us. So, this becomes a much simpler model. We just need the domain name, and a <a href="http://docs.python.org/library/pickle.html">pickled</a> RobotFileParser instance. We also need to know whether we're accessing an http or https and we'll give it <tt>type</tt> field to distinguish it from the <tt>Page</tt> model.

{% highlight python %}
class RobotsTxt(Document):
    type = TextField(default=&quot;robotstxt&quot;)
    domain = TextField()
    protocol = TextField()
    robot_parser_pickle = TextField()
{% endhighlight %}

We want to make the pickle/unpickle process transparent so we'll create a property that hides the underlying pickle representation. CouchDB can't store the binary pickle value, so we also base64 encode it and store that instead. If the object hasn't been set yet then we create a new one on the first access.

{% highlight python %}
    def _get_robot_parser(self):
        if self.robot_parser_pickle is not None:
            return pickle.loads(base64.b64decode(self.robot_parser_pickle))
        else:
            parser = RobotFileParser()
            parser.set_url(self.protocol + &quot;://&quot; + self.domain + &quot;/robots.txt&quot;)
            self.robot_parser = parser
            return parser
    def _set_robot_parser(self, parser):
        self.robot_parser_pickle = base64.b64encode(pickle.dumps(parser))
    robot_parser = property(_get_robot_parser, _set_robot_parser)
{% endhighlight %}

For both pages and <tt>robots.txt</tt> files we need to know whether we should reaccess the page. We'll do this by testing whether the we accessed the file in the last seven days of not. For Page models we do this by adding the following function which implements this check.

{% highlight python %}
    def is_valid(self):
        return (datetime.now() - self.last_checked).days &lt; 7
{% endhighlight %}

For the <tt>RobotsTxt</tt> we can take advantage of the last modified value stored in the <tt>RobotFileParser</tt> that we're wrapping. This is a unix timestamp so the <tt>is_valid</tt> function needs to be a little bit different, but follows the same pattern.

{% highlight python %}
    def is_valid(self):
        return (time.time() - self.robot_parser.mtime()) &lt; 7*24*60*60
{% endhighlight %}

To update the stored copy of a <tt>robots.txt</tt> we need to get the currently stored version, read a new one, set the last modified timestamp and then write it back to the database. To avoid hitting the same server too often we can use <a href="https://docs.djangoproject.com/en/dev/topics/cache/">Django's cache</a> to store a value for ten seconds, and sleep if that value already exists.

{% highlight python %}
    def update(self):
        while cache.get(self.domain) is not None:
            time.sleep(1)
        cache.set(self.domain, True, 10)
        parser = self.robot_parser
        parser.read()
        parser.modified()
        self.robot_parser = parser
        self.store(settings.db)
{% endhighlight %}

Once we've updated the stored file we need to be able to query it. This function just passes the URL being tested through to the underlying model along with our user agent string.

{% highlight python %}
    def is_allowed(self, url):
        return self.robot_parser.can_fetch(settings.USER_AGENT, url)
{% endhighlight %}

The final piece in our <tt>robots.txt</tt> puzzle is a function to pull the write object out of the database. We'll need a view that has the protocol and domain for each file as the key.

{% highlight python %}
    @staticmethod
    def get_by_domain(protocol, domain):
        r = settings.db.view(&quot;robotstxt/by_domain&quot;, key=[protocol, domain])
{% endhighlight %}

We query that mapping and if it returns a value then we load the object. If it's still valid then we can return right away, otherwise we need to update it.

{% highlight python %}
        if len(r) &gt; 0:
            doc = RobotsTxt.load(settings.db, r.rows[0].value)
            if doc.is_valid():
                return doc
{% endhighlight %}

If we've never loaded this domain's <tt>robots.txt</tt> file before then we need to create a blank object. The final step is to read the file and store it in the database.

{% highlight python %}
        else:
            doc = RobotsTxt(protocol=protocol, domain=domain)n
        doc.update()
        return doc
{% endhighlight %}

For completeness, here is the map file required for this function.

{% highlight python %}
function (doc) {
    if(doc.type == &quot;robotstxt&quot;) {
        emit([doc.protocol, doc.domain], doc._id);
    }
}
{% endhighlight %}

In this post we've discussed how to represent a webpage in our database as well as keep track of what paths we are and aren't allowed to access. We've also seen how to retrieve the <tt>robots.txt</tt> files and update them if they're too old.

Now that we can test whether we're allowed to access a URL in the next post in this series I'll show you how to begin crawling the web and populating our database.

Read <a href="/2012/01/12/back-garden-weather-in-couchdb-part-3/">part 3</a>.

<hr />
Photo of <a href="http://www.flickr.com/photos/johnnystiletto/5226474427/">Celery, Carrots &amp; Sweet Onion for Chicken Feet Stock</a> by <a href="http://www.flickr.com/photos/johnnystiletto/">I Believe I Can Fry</a>.n
