---
layout: post
title: CouchDB Document Cache
date: 2009-09-29 12:28:41.000000000 +01:00
type: post
parent_id: '0'
published: true
password: ''
status: publish
categories: []
tags:
- bulk insert
- couchdb
- database
meta:
  _edit_last: '364050'
author:
  login: andrewjw
  email: andrewjwilkinson@gmail.com
  display_name: Andrew Wilkinson
  first_name: Andrew
  last_name: Wilkinson
permalink: "/2009/09/29/couchdb-document-cache/"
---
<img src="{{ site.baseurl }}/assets/2654190796_c0a810ec44_m.jpg" alt="Red couch by daveaustria" style="float:right;" />It's well known that one of the best things you can do to speed up CouchDB is to use <a href="http://aartemenko.com/texts/couchdb-bulk-inserts-performance/">bulk inserts</a> to add or update many documents at one time.n
Bulk updates are easy to use if you're just blindly inserting documents into the database because you can just maintain a list of documents. However, a common scheme that I often use is to call a view to determine whether a document representing an object exists, update it if it does, add a new document if it doesn't. To help make this easier I use the <tt>DocCache</tt> class given below.n
The cache contains two interesting methods, <tt>get</tt> and <tt>update</tt>. Rather than writing directly to CouchDB when you want to add or update a document just pass the document to <tt>update</tt>. This will cache the document and periodically save them in a bulk update.n
It is possible that you will retrieve a document from CouchDB that an updated version exists in the cache. To avoid the possibility that changes get lost you should pass the retrieved document to <tt>get</tt>. This will either return the document you passed in or the document that's waiting to be saved if it exists in the cache. Because there is a gap between when you ask for document to be saved and when it actually is saved any views you use may be out of date, but that's the cost of faster updates with CouchDB.n
One complicating factor in the code is that the updating process updates the documents you passed in with <tt>_id</tt> and <tt>_rev</tt> from the newly saved documents. This means you can cache documents in a your own datastructure and should you decide to save the document again you won't get a conflict error because it will have been updated for you.n
[code]<br />
class DocCache:<br />
    def __init__(self, db, limit=1000):<br />
        self._db = db<br />
        self._cache = {}<br />
        self._new = []<br />
        self._limit = limit<br />
        self.inserted = 0n
    def __del__(self):<br />
        self.save()n
    def get(self, doc):<br />
        if &quot;_id&quot; in doc and doc[&quot;_id&quot;] in self._cache:<br />
            return self._cache[doc[&quot;_id&quot;]]<br />
        else:<br />
            return docn
    def update(self, doc, force_save=False):<br />
        if &quot;_id&quot; in doc:<br />
            self._cache[doc[&quot;_id&quot;]] = doc<br />
        else:<br />
            self._new.append(doc)n
        if force_save or len(self._cache) + len(self._new) &amp;gt; self._limit:<br />
            self.save()n
    def save(self):<br />
        docs = self._cache.values() + self._new<br />
        if len(docs) &gt; 0:<br />
            inserted_docs = self._db.update(docs)<br />
            for doc, newdoc in zip(docs, inserted_docs):<br />
                if newdoc[0]:<br />
                    doc[&quot;_id&quot;], doc[&quot;_rev&quot;] = newdoc[1], newdoc[2]<br />
                    self.inserted += 1<br />
            self._cache = {}<br />
            self._new = []<br />
[/code]n
<hr />
Photo of a <a href="http://www.flickr.com/photos/daveaustria/2654190796/">red couch</a> by <a href="http://www.flickr.com/photos/daveaustria">daveaustria</a>.n
