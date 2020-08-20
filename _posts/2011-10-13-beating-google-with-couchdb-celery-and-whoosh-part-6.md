---
layout: post
title: Beating Google With CouchDB, Celery and Whoosh (Part 6)
date: 2011-10-13 12:00:30.000000000 +01:00
type: post
tags:
- web development
- celery
- celerycrawler
- couchdb
- django
- whoosh
permalink: "/2011/10/13/beating-google-with-couchdb-celery-and-whoosh-part-6/"
flickr_user: 'https://www.flickr.com/photos/amortize/'
flickr_username: "amortize"
flickr_image: 'https://live.staticflickr.com/1179/527435776_a929bf88af_w.jpg'
flickr_imagelink: 'https://www.flickr.com/photos/amortize/527435776/'
flickr_imagename: 'Query'
---
We're nearing the end of our plot to create a Google-beating search engine (in my dreams at least) and in
this post we'll build the interface to query the index we've built up. Like Google the interface is very
simple, just a text box on one page and a list of results on another.

To begin with we just need a page with a query box. To make the page slightly more interesting we'll also
include the number of pages in the index, and a list of the top documents as ordered by our ranking algorithm.

In the templates on this page we reference `base.html` which provides the boiler plate code needed to
make an HTML page.

```python
{% raw %}
{% extends "base.html" %}
{% block body " %}
    <form action="/search" method="get">
        <input name="q" type="text">
        <input type="submit">
    </form>
    <hr>
    <p>{{ doc_count }} pages in index.</p>
    <hr>
    <h2>Top Pages</h2>
    <ol>
    {% for page in top_docs %}
        <li><a href="{{ page.url }}">{{ page.url }}</a> - {{ page.rank }}</li>
    {% endfor %}
    </ol>
{% endblock" %}
{% endraw %}
```

To show the number of pages in the index we need to count them. We've already created an view to list
`Page`s by their url and CouchDB can return the number of documents in a view without actually
returning any of them, so we can just get the count from that. We'll add the following function to the
`Page` model class.

```python
    @staticmethod
    def count():
        r = settings.db.view("page/by_url", limit=0)
        return r.total_rows
```

We also need to be able to get a list of the top pages, by rank. We just need to create view that has the
rank as the key and CouchDB will sort it for us automatically.

With all the background pieces in place the Django view function to render the index is really very
straightforward.

```python
def index(req):
    return render_to_response("index.html", { "doc_count": Page.count(), "top_docs": Page.get_top_by_rank(limit=20) })
```

Now we get to the meat of the experiment, the search results page. First we need to query the index.

```python
def search(req):
    q = QueryParser("content", schema=schema).parse(req.GET["q"])
```

This parses the user submitted query and prepares the query ready to be used by Whoosh. Next we need to pass
the parsed query to the index.

```python
    results = get_searcher().search(q, limit=100)
```

Hurrah! Now we have list of results that match our search query. All that remains is to decide what order to
display them in. To do this we normalize the score returned by Whoosh and the rank that we calculated, and add
them together.

```python
    if len(results) > 0:
        max_score = max([r.score for r in results])
        max_rank = max([r.fields()["rank"] for r in results])
```

To calculate our combined rank we normalize the score and the rank by setting the largest value of each to one
and scaling the rest appropriately.

```python
        combined = []
        for r in results:
            fields = r.fields()
            r.score = r.score/max_score
            r.rank = fields["rank"]/max_rank
            r.combined = r.score + r.rank
            combined.append(r)
```

The final stage is to sort our list by the combined score and render the results page.

```python
        combined.sort(key=lambda x: x.combined, reverse=True)
    else:
        combined = []
    return render_to_response("results.html", { "q": req.GET["q"], "results": combined })
```

The template for the results page is below.

```html
{% raw %}
{% extends "base.html" %}
{% block body %}
    <form action="/search" method="get">
        <input name="q" type="text" value="{{ q }}">
        <input type="submit">
    </form>
    {% for result in results|slice:":20"%}
        <p>
            <b><a href="{{ result.url }}">{{ result.title|safe }}</a></b> ({{ result.score }}, {{ result.rank }}, {{ result.combined }})<br>
            {{ result.desc|safe }}
        </p>
    {% endfor %}
{% endblock %}
{% endraw %}
```

So, there we have it. A complete web crawler, indexer and query website. In the next post I'll discuss how to
scale the search engine.

Read [part 7](/2011/10/19/beating-google-with-couchdb-celery-and-whoosh-part-7/).
