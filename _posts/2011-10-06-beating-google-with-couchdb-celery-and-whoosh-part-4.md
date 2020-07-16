---
layout: post
title: Beating Google With CouchDB, Celery and Whoosh (Part 4)
date: 2011-10-06 12:00:26.000000000 +01:00
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
meta:
  _edit_last: '364050'
  _wpas_done_twitter: '1'
author:
  login: andrewjw
  email: andrewjwilkinson@gmail.com
  display_name: Andrew Wilkinson
  first_name: Andrew
  last_name: Wilkinson
permalink: "/2011/10/06/beating-google-with-couchdb-celery-and-whoosh-part-4/"
---
<a href="http://www.flickr.com/photos/grismarengo/2516495079/"><img style="float:right;border:0;" src="{{ site.baseurl }}/assets/2516495079_a4c363f960_m.jpg" alt="Red Sofa encounter i" /></a>In this series I'm showing you how to build a webcrawler and search engine using standard Python based tools like Django, Celery and Whoosh with a CouchDB backend. In previous posts we created a data structure, parsed and stored <tt>robots.txt</tt> and stored a single webpage in our document. In this post I'll show you how to parse out the links from our stored HTML document so we can complete the crawler, and we'll start calculating the rank for the pages in our database.n
There are several different ways of parsing out the links in a given HTML document. You can just use a regular expression to pull the urls out, or you can use a more complete but also more complicated (and slower) method of parsing the HTML using the standard Python <a href="http://docs.python.org/library/htmlparser.html">htmlparser</a> library, or the wonderful <a href="http://www.crummy.com/software/BeautifulSoup/">Beautiful Soup</a>. The point of this series isn't to build a complete webcrawler, but to show you the basic building blocks. So, for simplicity's sake I'll use a regular expression. n
[code language="python"]<br />
link_single_re = re.compile(r&quot;&lt;a[^&gt;]+href='([^']+)'&quot;)<br />
link_double_re = re.compile(r'&lt;a[^&gt;]+href=&quot;([^&quot;]+)&quot;')<br />
[/code]n
All we need to look for an <tt>href</tt> attribute in an <tt>a</tt> tag. We'll use two regular expressions to handle single and double quotes, and then build a list containing all the links in the document.n
[code language="python"]<br />
@task<br />
def find_links(doc_id):<br />
    doc = Page.load(settings.db, doc_id)n
    raw_links = []<br />
    for match in link_single_re.finditer(doc.content):<br />
        raw_links.append(match.group(1))n
    for match in link_double_re.finditer(doc.content):<br />
        raw_links.append(match.group(1))<br />
[/code]n
Once we've got a list of the raw links we need to process them into absolute urls that we can send back to the <tt>retrieve_page</tt> task we wrote earlier. I'm cutting some corners with processing these urls, in particular I'm not dealing with <a href="http://www.w3.org/TR/html4/struct/links.html#h-12.4">base</a> tags.n
[code language="python"]<br />
    doc.links = []<br />
    for link in raw_links:<br />
        if link.startswith(&quot;#&quot;):<br />
            continue<br />
        elif link.startswith(&quot;http://&quot;) or link.startswith(&quot;https://&quot;):<br />
            pass<br />
        elif link.startswith(&quot;/&quot;):<br />
            parse = urlparse(doc[&quot;url&quot;])<br />
            link = parse.scheme + &quot;://&quot; + parse.netloc + link<br />
        else:<br />
            link = &quot;/&quot;.join(doc[&quot;url&quot;].split(&quot;/&quot;)[:-1]) + &quot;/&quot; + linkn
        doc.links.append(unescape(link.split(&quot;#&quot;)[0]))n
    doc.store(settings.db)<br />
[/code]n
Once we've got our list of links and saved the modified document we then need to trigger the next series of steps to occur. We need to calculate the rank of this page, so we trigger that task and then we step through each page that we linked to. If we've already got a copy of the page then we want to recalculate its rank to take into account the rank of this page (more on this later) and if we don't have a copy then we queue it up to be retrieved.n
[code language="python"]<br />
    calculate_rank.delay(doc.id)n
    for link in doc.links:<br />
        p = Page.get_id_by_url(link, update=False)<br />
        if p is not None:<br />
            calculate_rank.delay(p)<br />
        else:<br />
            retrieve_page.delay(link)<br />
[/code]n
We've now got a complete webcrawler. We can store webpages and <tt>robots.txt</tt> files. Given a starting URL our crawler will set about parsing pages to find out what they link to and retrieve those pages as well. Given enough time you'll end up with most of the internet on your harddisk!n
When we come to write the website to query the information we've collected we'll use two numbers to rank pages. First we'll use the a value that ranks pages base on the query used, but we'll also use a value that ranks pages based on their importance. This is the same method used by Google, known as <a href="http://en.wikipedia.org/wiki/Page_Rank">Page Rank</a>.n
Pank Rank is a measure of how likely you are to end up on a given page by clicking on a random link anywhere on the internet. The <a href="http://en.wikipedia.org/wiki/Page_Rank">Wikipedia article</a> goes into some detail on a number of ways to calculate it, but we'll use a very simple iterative algorithm.n
When created, a page is given a rank equal to <tt>1/number of pages</tt>. Each link that is found on a newly crawled page then causes the rank of the destination page to be calculated. In this case the rank of a page is the sum of the ranks of the pages that link to it, divided by the number of links on those pages, multiplied by a dampening factor (I use 0.85, but this could be adjusted.) If a page has a rank of 0.25 and has five links then each page linked to gains 0.05*0.85 rank for that link. If the change in rank of the page when recalculated is significant then the rank of all the pages it links to are recalculated.n
In this post we've completed the web crawler part of our search engine and discussed how to rank pages in importance. In the next post we'll implement this ranking and also create a full text index of the pages we have crawled.n
Read <a href="http://wp.me/pkxET-7s">part 5</a>.n
<hr />
Photo of <a href="http://www.flickr.com/photos/grismarengo/2516495079/">Red Sofa encounter i</a> by <a href="http://www.flickr.com/photos/grismarengo/">Ricard Gil</a>.n
