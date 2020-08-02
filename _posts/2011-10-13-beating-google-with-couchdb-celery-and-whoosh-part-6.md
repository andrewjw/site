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

In the templates on this page we reference <tt>base.html</tt> which provides the boiler plate code needed to
make an HTML page.

{% highlight python %}
{{ "{% extends &quot;base.html&quot; " }}%}
{{ "{% block body "}}%}
    &lt;form action=&quot;/search&quot; method=&quot;get&quot;&gt;
        &lt;input name=&quot;q&quot; type=&quot;text&quot;&gt;
        &lt;input type=&quot;submit&quot;&gt;
    &lt;/form&gt;
    &lt;hr&gt;
    &lt;p&gt;{{ doc_count }} pages in index.&lt;/p&gt;
    &lt;hr&gt;
    &lt;h2&gt;Top Pages&lt;/h2&gt;
    &lt;ol&gt;
    {% for page in top_docs %}
        &lt;li&gt;&lt;a href=&quot;{{ page.url }}&quot;&gt;{{ page.url }}&lt;/a&gt; - {{ page.rank }}&lt;/li&gt;
    {% endfor %}
    &lt;/ol&gt;
{{"{% endblock "}}%}
{% endhighlight %}

To show the number of pages in the index we need to count them. We've already created an view to list
<tt>Page</tt>s by their url and CouchDB can return the number of documents in a view without actually
returning any of them, so we can just get the count from that. We'll add the following function to the
<tt>Page</tt> model class.

{% highlight python %}
    @staticmethod
    def count():
        r = settings.db.view(&quot;page/by_url&quot;, limit=0)
        return r.total_rows
{% endhighlight %}

We also need to be able to get a list of the top pages, by rank. We just need to create view that has the
rank as the key and CouchDB will sort it for us automatically.

With all the background pieces in place the Django view function to render the index is really very
straightforward.

{% highlight python %}
def index(req):
    return render_to_response(&quot;index.html&quot;, { &quot;doc_count&quot;: Page.count(), &quot;top_docs&quot;: Page.get_top_by_rank(limit=20) })
{% endhighlight %}

Now we get to the meat of the experiment, the search results page. First we need to query the index.

{% highlight python %}
def search(req):
    q = QueryParser(&quot;content&quot;, schema=schema).parse(req.GET[&quot;q&quot;])
{% endhighlight %}

This parses the user submitted query and prepares the query ready to be used by Whoosh. Next we need to pass
the parsed query to the index.

{% highlight python %}
    results = get_searcher().search(q, limit=100)
{% endhighlight %}

Hurrah! Now we have list of results that match our search query. All that remains is to decide what order to
display them in. To do this we normalize the score returned by Whoosh and the rank that we calculated, and add
them together.

{% highlight python %}
    if len(results) &gt; 0:
        max_score = max([r.score for r in results])
        max_rank = max([r.fields()[&quot;rank&quot;] for r in results])
{% endhighlight %}

To calculate our combined rank we normalize the score and the rank by setting the largest value of each to one
and scaling the rest appropriately.

{% highlight python %}
        combined = []
        for r in results:
            fields = r.fields()
            r.score = r.score/max_score
            r.rank = fields[&quot;rank&quot;]/max_rank
            r.combined = r.score + r.rank
            combined.append(r)
{% endhighlight %}

The final stage is to sort our list by the combined score and render the results page.

{% highlight python %}
        combined.sort(key=lambda x: x.combined, reverse=True)
    else:
        combined = []
    return render_to_response(&quot;results.html&quot;, { &quot;q&quot;: req.GET[&quot;q&quot;], &quot;results&quot;: combined })
{% endhighlight %}

The template for the results page is below.

{% highlight html %}
{{"{% extends &quot;base.html&quot; "}}%}
{{"{% block body "}}%}
    &lt;form action=&quot;/search&quot; method=&quot;get&quot;&gt;
        &lt;input name=&quot;q&quot; type=&quot;text&quot; value=&quot;{{ q }}&quot;&gt;
        &lt;input type=&quot;submit&quot;&gt;
    &lt;/form&gt;
    {% for result in results|slice:&quot;:20&quot; %}
        &lt;p&gt;
            &lt;b&gt;&lt;a href=&quot;{{ result.url }}&quot;&gt;{{ result.title|safe }}&lt;/a&gt;&lt;/b&gt; ({{ result.score }}, {{ result.rank }}, {{ result.combined }})&lt;br&gt;
            {{ result.desc|safe }}
        &lt;/p&gt;
    {% endfor %}
{{"{% endblock "}}%}
{% endhighlight %}

So, there we have it. A complete web crawler, indexer and query website. In the next post I'll discuss how to
scale the search engine.

Read <a href="/2011/10/19/beating-google-with-couchdb-celery-and-whoosh-part-7/">part 7</a>.
