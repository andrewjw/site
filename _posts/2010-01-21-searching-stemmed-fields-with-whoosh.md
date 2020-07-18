---
layout: post
title: Searching Stemmed Fields With Whoosh
date: 2010-01-21 13:28:16.000000000 +00:00
type: post
tags:
- whoosh
- free text
- full text
- search
- stemming
permalink: "/2010/01/21/searching-stemmed-fields-with-whoosh/"
flickr_user: 'https://www.flickr.com/photos/feuilllu/'
flickr_username: Pierre Metivier
flickr_image: 'https://live.staticflickr.com/1431/739173692_70720e47f5_w.jpg'
flickr_imagelink: 'https://www.flickr.com/photos/feuilllu/739173692/'
flickr_imagename: WORDS
---
<a href="http://whoosh.ca/">Whoosh</a> is quite a nice pure-python full text search engine. While it is still being actively developed and is suitable for production usage there are still some rough edges. One problem that stumped me for a while was searching stemmed fields.

Stemming is where you take the endings off words, such as 'ings' on the word endings. This reduces the accuracy of searches but greatly increases the chances of users finding something related to what they were looking for.n
To create a stemmed field you need to tell Whoosh to use the <a href="http://packages.python.org/Whoosh/api/analysis.html#whoosh.analysis.StemmingAnalyzer"><tt>StemmingAnalyzer</tt></a>, as shown in the schema definition below.

    from whoosh.analysis import StemmingAnalyzer
    from whoosh.fields import Schema, TEXT, IDn
    schema = Schema(id=ID(stored=True, unique=True),
                           text=TEXT(analyzer=StemmingAnalyzer()))n

Using the <tt>StemmingAnalyzer</tt> will cause Whoosh to stem every word before it is added to the index. If you use the shortcut <a href="http://packages.python.org/Whoosh/api/searching.html#whoosh.searching.Searcher.search"><tt>search</tt></a> function to search with a word that should be stemmed it will return no results, as that word does not exist in the index, even though it was included in the data that was indexed.

To correctly search a stemmed index you must parse the query and tell the parse to use the <a href="http://packages.python.org/Whoosh/api/query.html#whoosh.query.Variations"><tt>Variations</tt></a> term class. The causes the words in the query to also be stemmed, so they correctly match words in the stemmed index.

    searcher = ix.searcher()
    qp = QueryParser(&quot;text&quot;, schema=schema, termclass=Variations)
    parsed = qp.parse(query)
    docs = searcher.search(parsed)
