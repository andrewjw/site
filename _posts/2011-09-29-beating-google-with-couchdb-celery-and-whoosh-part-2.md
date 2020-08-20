---
layout: post
title: 'Beating Google With CouchDB, Celery and Whoosh (Part 2)'
date: 2011-09-29 12:00:18.000000000 +01:00
tags:
  - web development
  - celery
  - celerycrawler
  - couchdb
  - django
  - python
  - whoosh
permalink: /2011/09/29/beating-google-with-couchdb-celery-and-whoosh-part-2/
flickr_user: 'https://www.flickr.com/photos/chasqui/'
flickr_username: "Luis Tamayo"
flickr_image: 'https://live.staticflickr.com/3956/14921715974_2d332ac18b_w.jpg'
flickr_imagelink: 'https://www.flickr.com/photos/chasqui/14921715974'
flickr_imagename: 'Carrots and Celery'
---
In this 
[series](/2011/09/27/beating-google-with-couchdb-celery-and-whoosh-part-1/)
I'll show you how to build a search engine using standard Python tools like Django, Whoosh and CouchDB. In
this post we'll begin by creating the data structure for storing the pages in the database, and write the
first parts of the webcrawler.

CouchDB's Python library has a simple [ORM system](http://packages.python.org/CouchDB/mapping.html)
that makes it easy to convert between the JSON objects stored in the database and a Python object.

To create the class you just need to specify the names of the fields, and their type. So, what do a search
engine need to store? The url is an obvious one, as is the content of the page. We also need to know when we
last accessed the page. To make things easier we'll also have a list of the urls that the page links to. One
of the great advantages of a database like CouchDB is that we don't need to create a separate table to hold
the links, we can just include them directly in the main document. To help return the best pages we'll use a
[page rank](http://en.wikipedia.org/wiki/PageRank) like algorithm to rank the page, so we also need
to store that rank. Finally, as is good practice on CouchDB we'll give the document a `type` field so
we can write views that only target this document type.

```python
class Page(Document):
    type = TextField(default=&quot;page&quot;)
    url = TextField()
    content = TextField()
    links = ListField(TextField())
    rank = FloatField(default=0)
    last_checked = DateTimeField(default=datetime.now)
```

That's a lot of description for not a lot of code! Just add that class to your `models.py` file. It's
not a normal Django model, but we're not using Django models in this project so it's the right place to put
it.

We also need to keep track of the urls that we are and aren't allowed to access. Fortunately for us Python
comes with a class, [RobotFileParser](http://docs.python.org/library/robotparser.html) which
handles the parsing of the file for us. So, this becomes a much simpler model. We just need the domain name,
and a [pickled](http://docs.python.org/library/pickle.html) RobotFileParser instance. We also need
to know whether we're accessing an http or https and we'll give it `type` field to distinguish it from
the `Page` model.

```python
class RobotsTxt(Document):
    type = TextField(default=&quot;robotstxt&quot;)
    domain = TextField()
    protocol = TextField()
    robot_parser_pickle = TextField()
```

We want to make the pickle/unpickle process transparent so we'll create a property that hides the underlying
pickle representation. CouchDB can't store the binary pickle value, so we also base64 encode it and store that
instead. If the object hasn't been set yet then we create a new one on the first access.

```python
    def _get_robot_parser(self):
        if self.robot_parser_pickle is not None:
            return pickle.loads(base64.b64decode(self.robot_parser_pickle))
        else:
            parser = RobotFileParser()
            parser.set_url(self.protocol + &quot;://&quot; + self.domain + &quot;/robots.txt&quot;) self.robot_parser = parser
            return parser

    def _set_robot_parser(self, parser):
        self.robot_parser_pickle = base64.b64encode(pickle.dumps(parser))
    robot_parser = property(_get_robot_parser, _set_robot_parser)
```

For both pages and `robots.txt` files we need to know whether we should reaccess the page. We'll do
this by testing whether the we accessed the file in the last seven days of not. For Page models we do this by
adding the following function which implements this check.

```python
    def is_valid(self):
        return (datetime.now() - self.last_checked).days &lt; 7
```

For the `RobotsTxt` we can take advantage of the last modified value stored in the
`RobotFileParser` that we're wrapping. This is a unix timestamp so the `is_valid` function needs
to be a little bit different, but follows the same pattern.

```python
    def is_valid(self):
        return (time.time() - self.robot_parser.mtime()) &lt; 7*24*60*60
```

To update the stored copy of a `robots.txt` we need to get the currently stored version, read a new
one, set the last modified timestamp and then write it back to the database. To avoid hitting the same server
too often we can use [Django's cache](https://docs.djangoproject.com/en/dev/topics/cache/) to store
a value for ten seconds, and sleep if that value already exists.

```python
    def update(self):
        while cache.get(self.domain) is not None: time.sleep(1)
        cache.set(self.domain, True, 10)
        parser = self.robot_parser
        parser.read()
        parser.modified()
        self.robot_parser = parser
        self.store(settings.db)
```

Once we've updated the stored file we need to be able to query it. This function just passes the URL being
tested through to the underlying model along with our user agent string.

```python
def is_allowed(self, url):
    return self.robot_parser.can_fetch(settings.USER_AGENT, url)
```

The final piece in our `robots.txt` puzzle is a function to pull the write object out of the database.
We'll need a view that has the protocol and domain for each file as the key.

```python
@staticmethod
def get_by_domain(protocol, domain):
    r = settings.db.view(&quot;robotstxt/by_domain&quot;, key=[protocol, domain])
```

We query that mapping and if it returns a value then we load the object. If it's still valid then we can
return right away, otherwise we need to update it.

```python
    if len(r) &gt; 0:
        doc = RobotsTxt.load(settings.db, r.rows[0].value)
        if doc.is_valid():
        return doc
```

If we've never loaded this domain's `robots.txt` file before then we need to create a blank object. The
final step is to read the file and store it in the database.

```python
    else:
        doc = RobotsTxt(protocol=protocol, domain=domain)n doc.update()
        return doc
```

For completeness, here is the map file required for this function.

```javascript
    function (doc) {
        if(doc.type == &quot;robotstxt&quot;) {
            emit([doc.protocol, doc.domain], doc._id);
        }
    }
```

In this post we've discussed how to represent a webpage in our database as well as keep track of what paths we
are and aren't allowed to access. We've also seen how to retrieve the `robots.txt` files and update
them if they're too old.

Now that we can test whether we're allowed to access a URL in the next post in this series I'll show you how
to begin crawling the web and populating our database.

Read [part 3](/2012/01/12/back-garden-weather-in-couchdb-part-3/).
