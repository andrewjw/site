---
layout: post
title: Beating Google With CouchDB, Celery and Whoosh (Part 6)
date: 2011-10-13 12:00:30.000000000 +01:00
type: post
parent_id: '0'
published: true
password: ''
status: publish
categories:
- web development
tags:
- celery
- celerycrawler
- couchdb
- django
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
permalink: "/2011/10/13/beating-google-with-couchdb-celery-and-whoosh-part-6/"
---
<a href="http://www.flickr.com/photos/amortize/527435776/"><img style="float:right;border:0;" src="{{ site.baseurl }}/assets/527435776_a929bf88af_m.jpg" alt="Query" /></a>We're nearing the end of our plot to create a Google-beating search engine (in my dreams at least) and in this post we'll build the interface to query the index we've built up. Like Google the interface is very simple, just a text box on one page and a list of results on another.n
To begin with we just need a page with a query box. To make the page slightly more interesting we'll also include the number of pages in the index, and a list of the top documents as ordered by our ranking algorithm.n
In the templates on this page we reference <tt>base.html</tt> which provides the boiler plate code needed to make an HTML page.n
[code language="html"]<br />
{{ "{% extends &quot;base.html&quot; " }}%}n
{{ "{% block body "}}%}<br />
    &lt;form action=&quot;/search&quot; method=&quot;get&quot;&gt;<br />
        &lt;input name=&quot;q&quot; type=&quot;text&quot;&gt;<br />
        &lt;input type=&quot;submit&quot;&gt;<br />
    &lt;/form&gt;n
    &lt;hr&gt;n
    &lt;p&gt;{{ doc_count }} pages in index.&lt;/p&gt;n
    &lt;hr&gt;n
    &lt;h2&gt;Top Pages&lt;/h2&gt;n
    &lt;ol&gt;<br />
    {% for page in top_docs %}<br />
        &lt;li&gt;&lt;a href=&quot;{{ page.url }}&quot;&gt;{{ page.url }}&lt;/a&gt; - {{ page.rank }}&lt;/li&gt;<br />
    {% endfor %}<br />
    &lt;/ol&gt;<br />
{{"{% endblock "}}%}<br />
[/code]n
To show the number of pages in the index we need to count them. We've already created an view to list <tt>Page</tt>s by their url and CouchDB can return the number of documents in a view without actually returning any of them, so we can just get the count from that. We'll add the following function to the <tt>Page</tt> model class.n
[code language="python"]<br />
    @staticmethod<br />
    def count():<br />
        r = settings.db.view(&quot;page/by_url&quot;, limit=0)<br />
        return r.total_rows<br />
[/code]n
We also need to be able to get a list of the top pages, by rank. We just need to create view that has the rank as the key and CouchDB will sort it for us automatically.n
With all the background pieces in place the Django view function to render the index is really very straightforward.n
[code language="python"]<br />
def index(req):<br />
    return render_to_response(&quot;index.html&quot;, { &quot;doc_count&quot;: Page.count(), &quot;top_docs&quot;: Page.get_top_by_rank(limit=20) })<br />
[/code]n
Now we get to the meat of the experiment, the search results page. First we need to query the index.n
[code language="python"]<br />
def search(req):<br />
    q = QueryParser(&quot;content&quot;, schema=schema).parse(req.GET[&quot;q&quot;])<br />
[/code]n
This parses the user submitted query and prepares the query ready to be used by Whoosh. Next we need to pass the parsed query to the index.n
[code language="python"]<br />
    results = get_searcher().search(q, limit=100)<br />
[/code]n
Hurrah! Now we have list of results that match our search query. All that remains is to decide what order to display them in. To do this we normalize the score returned by Whoosh and the rank that we calculated, and add them together.n
[code language="python"]<br />
    if len(results) &gt; 0:<br />
        max_score = max([r.score for r in results])<br />
        max_rank = max([r.fields()[&quot;rank&quot;] for r in results])<br />
[/code]n
To calculate our combined rank we normalize the score and the rank by setting the largest value of each to one and scaling the rest appropriately.n
[code language="python"]<br />
        combined = []<br />
        for r in results:<br />
            fields = r.fields()<br />
            r.score = r.score/max_score<br />
            r.rank = fields[&quot;rank&quot;]/max_rank<br />
            r.combined = r.score + r.rank<br />
            combined.append(r)<br />
[/code]n
The final stage is to sort our list by the combined score and render the results page.n
[code language="python"]<br />
        combined.sort(key=lambda x: x.combined, reverse=True)<br />
    else:<br />
        combined = []n
    return render_to_response(&quot;results.html&quot;, { &quot;q&quot;: req.GET[&quot;q&quot;], &quot;results&quot;: combined })<br />
[/code]n
The template for the results page is below.n
[code language="html"]<br />
{{"{% extends &quot;base.html&quot; "}}%}n
{{"{% block body "}}%}<br />
    &lt;form action=&quot;/search&quot; method=&quot;get&quot;&gt;<br />
        &lt;input name=&quot;q&quot; type=&quot;text&quot; value=&quot;{{ q }}&quot;&gt;<br />
        &lt;input type=&quot;submit&quot;&gt;<br />
    &lt;/form&gt;n
    {% for result in results|slice:&quot;:20&quot; %}<br />
        &lt;p&gt;<br />
            &lt;b&gt;&lt;a href=&quot;{{ result.url }}&quot;&gt;{{ result.title|safe }}&lt;/a&gt;&lt;/b&gt; ({{ result.score }}, {{ result.rank }}, {{ result.combined }})&lt;br&gt;<br />
            {{ result.desc|safe }}<br />
        &lt;/p&gt;<br />
    {% endfor %}<br />
{{"{% endblock "}}%}<br />
[/code]n
So, there we have it. A complete web crawler, indexer and query website. In the next post I'll discuss how to scale the search engine.n
Read <a href="http://wp.me/pkxET-7E">part 7</a>.n
<hr />
Photo of <a href="http://www.flickr.com/photos/amortize/527435776/">Query</a> by <a href="http://www.flickr.com/photos/amortize/">amortize</a>.n
