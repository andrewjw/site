---
layout: post
title: Beating Google With CouchDB, Celery and Whoosh (Part 4)
date: 2011-10-06 12:00:26.000000000 +01:00
type: post
tags:
- web development
- celery
- celerycrawler
- couchdb
- django
permalink: "/2011/10/06/beating-google-with-couchdb-celery-and-whoosh-part-4/"
flickr_user: 'https://www.flickr.com/photos/grismarengo/'
flickr_username: "Ricard Gil"
flickr_image: 'https://live.staticflickr.com/2039/2516495079_a4c363f960_z.jpg'
flickr_imagelink: 'https://www.flickr.com/photos/grismarengo/2516495079/'
flickr_imagename: 'Red Sofa encounter i'
---
In this series I'm showing you how to build a webcrawler and search engine using standard Python based tools
like Django, Celery and Whoosh with a CouchDB backend. In previous posts we created a data structure, parsed
and stored <tt>robots.txt</tt> and stored a single webpage in our document. In this post I'll show you how to
parse out the links from our stored HTML document so we can complete the crawler, and we'll start calculating
the rank for the pages in our database.

There are several different ways of parsing out the links in a given HTML document. You can just use a regular
expression to pull the urls out, or you can use a more complete but also more complicated (and slower) method
of parsing the HTML using the standard Python <a
href="http://docs.python.org/library/htmlparser.html">htmlparser</a> library, or the wonderful <a
href="http://www.crummy.com/software/BeautifulSoup/">Beautiful Soup</a>. The point of this series isn't to
build a complete webcrawler, but to show you the basic building blocks. So, for simplicity's sake I'll use a
regular expression.

{% highlight python %} link_single_re = re.compile(r&quot;&lt;a[^&gt;]+href='([^']+)'&quot;) link_double_re =
re.compile(r'&lt;a[^&gt;]+href=&quot;([^&quot;]+)&quot;') {% endhighlight %}

All we need to look for an <tt>href</tt> attribute in an <tt>a</tt> tag. We'll use two regular expressions to
handle single and double quotes, and then build a list containing all the links in the document.

{% highlight python %} @task<br /> def find_links(doc_id): doc = Page.load(settings.db, doc_id) raw_links = []
for match in link_single_re.finditer(doc.content): raw_links.append(match.group(1)) for match in
link_double_re.finditer(doc.content): raw_links.append(match.group(1)) {% endhighlight %}

Once we've got a list of the raw links we need to process them into absolute urls that we can send back to the
<tt>retrieve_page</tt> task we wrote earlier. I'm cutting some corners with processing these urls, in
particular I'm not dealing with <a href="http://www.w3.org/TR/html4/struct/links.html#h-12.4">base</a> tags.

{% highlight python %} doc.links = [] for link in raw_links: if link.startswith(&quot;#&quot;): continue elif
link.startswith(&quot;http://&quot;) or link.startswith(&quot;https://&quot;): pass elif
link.startswith(&quot;/&quot;): parse = urlparse(doc[&quot;url&quot;]) link = parse.scheme + &quot;://&quot; +
parse.netloc + link else: link = &quot;/&quot;.join(doc[&quot;url&quot;].split(&quot;/&quot;)[:-1]) +
&quot;/&quot; + link doc.links.append(unescape(link.split(&quot;#&quot;)[0])) doc.store(settings.db) {%
endhighlight %}

Once we've got our list of links and saved the modified document we then need to trigger the next series of
steps to occur. We need to calculate the rank of this page, so we trigger that task and then we step through
each page that we linked to. If we've already got a copy of the page then we want to recalculate its rank to
take into account the rank of this page (more on this later) and if we don't have a copy then we queue it up
to be retrieved.

{% highlight python %} calculate_rank.delay(doc.id) for link in doc.links: p = Page.get_id_by_url(link,
update=False) if p is not None: calculate_rank.delay(p) else: retrieve_page.delay(link) {% endhighlight %}

We've now got a complete webcrawler. We can store webpages and <tt>robots.txt</tt> files. Given a starting URL
our crawler will set about parsing pages to find out what they link to and retrieve those pages as well. Given
enough time you'll end up with most of the internet on your harddisk!

When we come to write the website to query the information we've collected we'll use two numbers to rank
pages. First we'll use the a value that ranks pages base on the query used, but we'll also use a value that
ranks pages based on their importance. This is the same method used by Google, known as <a
href="http://en.wikipedia.org/wiki/Page_Rank">Page Rank</a>.

Pank Rank is a measure of how likely you are to end up on a given page by clicking on a random link anywhere
on the internet. The <a href="http://en.wikipedia.org/wiki/Page_Rank">Wikipedia article</a> goes into some
detail on a number of ways to calculate it, but we'll use a very simple iterative algorithm.

When created, a page is given a rank equal to <tt>1/number of pages</tt>. Each link that is found on a newly
crawled page then causes the rank of the destination page to be calculated. In this case the rank of a page is
the sum of the ranks of the pages that link to it, divided by the number of links on those pages, multiplied
by a dampening factor (I use 0.85, but this could be adjusted.) If a page has a rank of 0.25 and has five
links then each page linked to gains 0.05*0.85 rank for that link. If the change in rank of the page when
recalculated is significant then the rank of all the pages it links to are recalculated.

In this post we've completed the web crawler part of our search engine and discussed how to rank pages in
importance. In the next post we'll implement this ranking and also create a full text index of the pages we
have crawled.

Read <a href="/2011/10/11/beating-google-with-couchdb-celery-and-whoosh-part-5/">part 5</a>.
