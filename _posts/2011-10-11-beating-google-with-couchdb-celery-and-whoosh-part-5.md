---
layout: post
title: Beating Google With CouchDB, Celery and Whoosh (Part 5)
date: 2011-10-11 12:00:16.000000000 +01:00
type: post
tags:
- web development
- celery
- celerycrawler
- couchdb
- django
- whoosh
permalink: "/2011/10/11/beating-google-with-couchdb-celery-and-whoosh-part-5/"
flickr_user: 'https://www.flickr.com/photos/mini_malist/'
flickr_username: "mini malist"
flickr_image: 'https://live.staticflickr.com/65535/49076745823_b23d32d76c_w.jpg'
flickr_imagelink: 'https://www.flickr.com/photos/mini_malist/49076745823/'
flickr_imagename: 'order'
---
In this post we'll continue building the backend for our search engine by implementing the algorithm we
designed in the last post for ranking pages. We'll also build a index of our pages with
[Whoosh](https://bitbucket.org/mchaput/whoosh/wiki/Home), a pure-Python full-text indexer and
query engine.

To calculate the rank of a page we need to know what other pages link to a given url, and how many links that
page has. The code below is a CouchDB map called `page/links_to_url`. For each page this will output a
row for each link on the page with the url linked to as the key and the page's rank and number of links as the
value.

```python
function (doc) {
    if(doc.type == &quot;page&quot;) {
        for(i = 0; i &lt; doc.links.length; i++) {
            emit(doc.links[i], [doc.rank, doc.links.length]);
        }
    }
}
```

As before we're using a Celery task to allow us to distribute our calculations. When we wrote the
`find_links` task we called `calculate_rank` with the document id for our page as the parameter.

```python
@task
def calculate_rank(doc_id):
    page = Page.load(settings.db, doc_id)
```

Next we get a list of ranks for the page's that link to this page. This static method is a thin wrapper around
the `page/links_to_url` map function given above.

```python
    links = Page.get_links_to_url(page.url)
```

Now we have the list of ranks we can calculate the rank of this page by dividing the rank of the linking page
by the number of links and summing this across all the linking pages.

```python
    rank = 0
    for link in links:
        rank += link[0] / link[1]
```

To prevent cycles (where `A` links to `B` and `B` links to `A`) from causing an
infinite loop in our calculation we apply a damping factor. This causes the value of the link to decline by
0.85 and combined with the limit later in the function will force any loops to settle on a value.

```python
    old_rank = page.rank
    page.rank = rank * 0.85
```

If we didn't find any links to this page then we give it a default rank of `1/number_of_pages`.

```python
    if page.rank == 0:
        page.rank = 1.0/settings.db.view(&quot;page/by_url&quot;, limit=0).total_rows
```

Finally we compare the new rank to the previous rank in our system. If it has changed by more than 0.0001 then
we save the new rank and cause all the pages linked to from our page to recalculate their rank.

```python
    if abs(old_rank - page.rank) &gt; 0.0001:
        page.store(settings.db)
        for link in page.links:
            p = Page.get_id_by_url(link, update=False)
            if p is not None:
                calculate_rank.delay(p)
```

This is a very simplistic implementation of a page rank algorithm. It does generate a useful ranking of pages,
but the number of queued `calculate_rank` tasks explodes. In a later post I'll discuss how this could
be made rewritten to be more efficient.

[Whoosh](https://bitbucket.org/mchaput/whoosh/wiki/Home) is a pure-Python full text search engine.
In the next post we'll look at querying it, but first we need to index the pages we've crawled.

The first step with Whoosh is to specify your schema. To speed up the display of results we store the
information we need to render the results page directly in the schema. For this we need the page title, url
and description. We also store the score given to the page by our pagerank-like algorithm. Finally we add
the page text to the index so we can query it. If you want more details, the
[Whoosh documentation](http://packages.python.org/Whoosh/) is pretty good.

```python
from whoosh.fields import *n
schema = Schema(title=TEXT(stored=True), url=ID(stored=True, unique=True), desc=ID(stored=True), rank=NUMERIC(stored=True, type=float), content=TEXT)
```

CouchDB provides an interface for being informed whenever a document in the database
[changes](http://guide.couchdb.org/draft/notifications.html). This is perfect for building an
index.

Our full-text indexing daemon is implemented as a Django management command so there is some boilerplate code
required to make this work.

```python
class Command(BaseCommand):
    def handle(self, **options):
        since = get_last_change()
        writer = get_writer()
```

CouchDB allows you to get all the changes that have occurred since a specific point in time (using a revision
number). We store this number inside the Whoosh index directory, and accessing it using the
`get_last_change` and `set_last_change` functions. Our access to the Whoosh index is through a
[IndexWriter](http://packages.python.org/Whoosh/quickstart.html#the-indexwriter-object) object,
again accessed through an abstraction function.

Now we enter an infinite loop and call the `changes` function on our CouchDB database object to get
the changes.

```python
        try:
            while True:
                changes = settings.db.changes(since=since)
                since = changes[&quot;last_seq&quot;]
                for changeset in changes[&quot;results&quot;]:
                    try:
                        doc = settings.db[changeset[&quot;id&quot;]]
                    except couchdb.http.ResourceNotFound:
                        continue
```

In our database we store `robots.txt` files as well as pages, so we need to ignore them. We also need
to parse the document so we can pull out the text from the page. We do this with the
[BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/) library.

```python
                    if &quot;type&quot; in doc and doc[&quot;type&quot;] == &quot;page&quot;:
                        soup = BeautifulSoup(doc[&quot;content&quot;])
                        if soup.body is None:
                            continue
```

On the results page we try to use the meta description if we can find it.

```python
                        desc = soup.findAll('meta', attrs={ &quot;name&quot;: desc_re })
```

Once we've got the parsed document we update our Whoosh index. The code is a little complicated because we
need to handle the case where the page doesn't have a title or description, and that we search for the title
as well as the body text of the page. The key element here is `text=True` which pulls out just the
text from a node and strips out all of the tags.

```python
                        writer.update_document(
                                title=unicode(soup.title(text=True)[0]) if soup.title is not None and len(soup.title(text=True)) &gt; 0 else doc[&quot;url&quot;],
                                url=unicode(doc[&quot;url&quot;]),
                                desc=unicode(desc[0][&quot;content&quot;]) if len(desc) &gt; 0 and desc[0][&quot;content&quot;] is not None else u&quot;&quot;,
                                rank=doc[&quot;rank&quot;],
                                content=unicode(soup.title(text=True)[0] + &quot;\n&quot; + doc[&quot;url&quot;] + &quot;\n&quot; + &quot;&quot;.join(soup.body(text=True)))
                            )
```

Finally we update the index and save the last change number so next time the script is run we continue from
where we left off.

```python
                    writer.commit()
                    writer = get_writer()
                set_last_change(since)
        finally:
            set_last_change(since)
```

In the next post I'll discuss how to query the index, sort the documents by our two rankings and build a
simple web interface.

Read [part 6](/2011/10/13/beating-google-with-couchdb-celery-and-whoosh-part-6/).
