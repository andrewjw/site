---
layout: post
title: Beating Google With CouchDB, Celery and Whoosh (Part 5)
date: 2011-10-11 12:00:16.000000000 +01:00
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
  twitter_cards_summary_img_size: a:7:{i:0;i:240;i:1;i:180;i:2;i:2;i:3;s:24:"width="240"
    height="180"";s:4:"bits";i:8;s:8:"channels";i:3;s:4:"mime";s:10:"image/jpeg";}
  _oembed_0edb3797b8e8f30eb81c5531a5433564: "{{unknown}}"
  _oembed_cd3e5a7a7c263d60541f8dabb1fd2242: "{{unknown}}"
  _oembed_cc6590d1f6098a9be554862a540d76ae: "{{unknown}}"
  _oembed_48f981e5b2ca43e5f70e79bc9c186d09: "{{unknown}}"
  _oembed_12c6af3f430c10f5c0690ea6ecf36ad5: "{{unknown}}"
  _oembed_cca4158b572669f387b1f0568fa15365: "{{unknown}}"
  _oembed_92c0385e49af32d7cf8a1e79306ffa6a: "{{unknown}}"
  _oembed_3c1c9f1a621b3ad49a98ad09c8187da9: "{{unknown}}"
  _oembed_e8617c8bf4633247c2aa1ce1b76ab288: "{{unknown}}"
  _oembed_37a4f2e8ac75052e6597869acc053b1f: "{{unknown}}"
author:
  login: andrewjw
  email: andrewjwilkinson@gmail.com
  display_name: Andrew Wilkinson
  first_name: Andrew
  last_name: Wilkinson
permalink: "/2011/10/11/beating-google-with-couchdb-celery-and-whoosh-part-5/"
---
<a href="http://www.flickr.com/photos/flyzipper/61475775/"><img style="float:right;border:0;" src="{{ site.baseurl }}/assets/61475775_6b823a6db7_m.jpg" alt="order" /></a>In this post we'll continue building the backend for our search engine by implementing the algorithm we designed in the last post for ranking pages. We'll also build a index of our pages with <a href="https://bitbucket.org/mchaput/whoosh/wiki/Home">Whoosh</a>, a pure-Python full-text indexer and query engine.n
To calculate the rank of a page we need to know what other pages link to a given url, and how many links that page has. The code below is a CouchDB map called <tt>page/links_to_url</tt>. For each page this will output a row for each link on the page with the url linked to as the key and the page's rank and number of links as the value.n
[code language="javascript"]<br />
function (doc) {<br />
    if(doc.type == &quot;page&quot;) {<br />
        for(i = 0; i &lt; doc.links.length; i++) {<br />
            emit(doc.links[i], [doc.rank, doc.links.length]);<br />
        }<br />
    }<br />
}<br />
[/code]n
As before we're using a Celery task to allow us to distribute our calculations. When we wrote the <tt>find_links</tt> task we called <tt>calculate_rank</tt> with the document id for our page as the parameter.n
[code language="python"]<br />
@task<br />
def calculate_rank(doc_id):<br />
    page = Page.load(settings.db, doc_id)<br />
[/code]n
Next we get a list of ranks for the page's that link to this page. This static method is a thin wrapper around the <tt>page/links_to_url</tt> map function given above.n
[code language="python"]<br />
    links = Page.get_links_to_url(page.url)<br />
[/code]n
Now we have the list of ranks we can calculate the rank of this page by dividing the rank of the linking page by the number of links and summing this across all the linking pages.n
[code language="python"]<br />
    rank = 0<br />
    for link in links:<br />
        rank += link[0] / link[1]<br />
[/code]n
To prevent cycles (where <tt>A</tt> links to <tt>B</tt> and <tt>B</tt> links to <tt>A</tt>) from causing an infinite loop in our calculation we apply a damping factor. This causes the value of the link to decline by 0.85 and combined with the limit later in the function will force any loops to settle on a value.n
[code language="python"]<br />
    old_rank = page.rank<br />
    page.rank = rank * 0.85<br />
[/code]n
If we didn't find any links to this page then we give it a default rank of <tt>1/number_of_pages</tt>.n
[code language="python"]<br />
    if page.rank == 0:<br />
        page.rank = 1.0/settings.db.view(&quot;page/by_url&quot;, limit=0).total_rows<br />
[/code]n
Finally we compare the new rank to the previous rank in our system. If it has changed by more than 0.0001 then we save the new rank and cause all the pages linked to from our page to recalculate their rank.n
[code language="python"]<br />
    if abs(old_rank - page.rank) &gt; 0.0001:<br />
        page.store(settings.db)n
        for link in page.links:<br />
            p = Page.get_id_by_url(link, update=False)<br />
            if p is not None:<br />
                calculate_rank.delay(p)<br />
[/code]n
This is a very simplistic implementation of a page rank algorithm. It does generate a useful ranking of pages, but the number of queued <tt>calculate_rank</tt> tasks explodes. In a later post I'll discuss how this could be made rewritten to be more efficient.n
<a href="https://bitbucket.org/mchaput/whoosh/wiki/Home">Whoosh</a> is a pure-Python full text search engine. In the next post we'll look at querying it, but first we need to index the pages we've crawled.n
The first step with Whoosh is to specify your schema. To speed up the display of results we store the information we need to render the results page directly in the schema. For this we need the page title, url and description. We also store the score given to the page by our pagerank-like algorithm. Finally we add the page text to the index so we can query it. If you want more details, the <a href="http://packages.python.org/Whoosh/">Whoosh documentation</a> is pretty good.n
[code language="python"]<br />
from whoosh.fields import *n
schema = Schema(title=TEXT(stored=True), url=ID(stored=True, unique=True), desc=ID(stored=True), rank=NUMERIC(stored=True, type=float), content=TEXT)<br />
[/code]n
CouchDB provides an interface for being informed whenever a document in the database <a href="http://guide.couchdb.org/draft/notifications.html">changes</a>. This is perfect for building an index.n
Our full-text indexing daemon is implemented as a Django management command so there is some boilerplate code required to make this work.n
[code language="python"]<br />
class Command(BaseCommand):<br />
    def handle(self, **options):<br />
        since = get_last_change()<br />
        writer = get_writer()<br />
[/code]n
CouchDB allows you to get all the changes that have occurred since a specific point in time (using a revision number). We store this number inside the Whoosh index directory, and accessing it using the <tt>get_last_change</tt> and <tt>set_last_change</tt> functions. Our access to the Whoosh index is through a <a href="http://packages.python.org/Whoosh/quickstart.html#the-indexwriter-object">IndexWriter</a> object, again accessed through an abstraction function.n
Now we enter an infinite loop and call the <tt>changes</tt> function on our CouchDB database object to get the changes.n
[code language="python"]<br />
        try:<br />
            while True:<br />
                changes = settings.db.changes(since=since)<br />
                since = changes[&quot;last_seq&quot;]<br />
                for changeset in changes[&quot;results&quot;]:<br />
                    try:<br />
                        doc = settings.db[changeset[&quot;id&quot;]]<br />
                    except couchdb.http.ResourceNotFound:<br />
                        continue<br />
[/code]n
In our database we store <tt>robots.txt</tt> files as well as pages, so we need to ignore them. We also need to parse the document so we can pull out the text from the page. We do this with the <a href="http://www.crummy.com/software/BeautifulSoup/">BeautifulSoup</a> library.n
[code language="python"]<br />
                    if &quot;type&quot; in doc and doc[&quot;type&quot;] == &quot;page&quot;:<br />
                        soup = BeautifulSoup(doc[&quot;content&quot;])<br />
                        if soup.body is None:<br />
                            continue<br />
[/code]n
On the results page we try to use the meta description if we can find it.n
[code language="python"]<br />
                        desc = soup.findAll('meta', attrs={ &quot;name&quot;: desc_re })<br />
[/code]n
Once we've got the parsed document we update our Whoosh index. The code is a little complicated because we need to handle the case where the page doesn't have a title or description, and that we search for the title as well as the body text of the page. The key element here is <tt>text=True</tt> which pulls out just the text from a node and strips out all of the tags.n
[code language="python"]<br />
                        writer.update_document(<br />
                                title=unicode(soup.title(text=True)[0]) if soup.title is not None and len(soup.title(text=True)) &gt; 0 else doc[&quot;url&quot;],<br />
                                url=unicode(doc[&quot;url&quot;]),<br />
                                desc=unicode(desc[0][&quot;content&quot;]) if len(desc) &gt; 0 and desc[0][&quot;content&quot;] is not None else u&quot;&quot;,<br />
                                rank=doc[&quot;rank&quot;],<br />
                                content=unicode(soup.title(text=True)[0] + &quot;\n&quot; + doc[&quot;url&quot;] + &quot;\n&quot; + &quot;&quot;.join(soup.body(text=True)))<br />
                            )<br />
[/code]n
Finally we update the index and save the last change number so next time the script is run we continue from where we left off.n
[code language="python"]<br />
                    writer.commit()<br />
                    writer = get_writer()n
                set_last_change(since)<br />
        finally:<br />
            set_last_change(since)<br />
[/code]n
In the next post I'll discuss how to query the index, sort the documents by our two rankings and build a simple web interface.n
Read <a href="http://wp.me/pkxET-7B">part 6</a>.n
<hr />
Photo of <a href="http://www.flickr.com/photos/flyzipper/61475775/">order</a> by <a href="http://www.flickr.com/photos/flyzipper/">Steve Mishos</a>.n