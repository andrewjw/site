---
layout: post
title: CouchDB Document Cache
date: 2009-09-29 12:28:41.000000000 +01:00
type: post
tags:
- couchdb
- database
permalink: "/2009/09/29/couchdb-document-cache/"
flickr_user: 'https://www.flickr.com/photos/moneyblognewz/'
flickr_username: Money Blog Newz
flickr_image: 'https://live.staticflickr.com/5006/5325312286_7d7177837f_w.jpg'
flickr_imagelink: 'http://www.flickr.com/photos/daveaustria/2654190796/'
flickr_imagename: Living room
---
It's well known that one of the best things you can do to speed up CouchDB is to use [bulk
inserts](http://aartemenko.com/texts/couchdb-bulk-inserts-performance/) to add or update many documents at one
time.

Bulk updates are easy to use if you're just blindly inserting documents into the database because you can just
maintain a list of documents. However, a common scheme that I often use is to call a view to determine whether
a document representing an object exists, update it if it does, add a new document if it doesn't. To help make
this easier I use the `DocCache` class given below.

The cache contains two interesting methods, `get` and `update`. Rather than writing directly to CouchDB when
you want to add or update a document just pass the document to `update`. This will cache the document and
periodically save them in a bulk update.

It is possible that you will retrieve a document from CouchDB that an updated version exists in the cache. To
avoid the possibility that changes get lost you should pass the retrieved document to `get`. This will either
return the document you passed in or the document that's waiting to be saved if it exists in the cache.
Because there is a gap between when you ask for document to be saved and when it actually is saved any views
you use may be out of date, but that's the cost of faster updates with CouchDB.

One complicating factor in the code is that the updating process updates the documents you passed in with
`_id` and `_rev` from the newly saved documents. This means you can cache documents in a your own
datastructure and should you decide to save the document again you won't get a conflict error because it will
have been updated for you.

```python
class DocCache:
    def __init__(self, db, limit=1000):
        self._db = db
        self._cache = {}
        self._new = []
        self._limit = limit
        self.inserted = 0

    def __del__(self):
        self.save()

    def get(self, doc):
        if "_id" in doc and doc["_id"] in self._cache:
            return self._cache[doc["_id"]]
        else:
            return doc

    def update(self, doc, force_save=False):
        if "_id" in doc:
            self._cache[doc["_id"]] = doc
        else:
            self._new.append(doc)
        if force_save or len(self._cache) + len(self._new) > self._limit:
            self.save()

    def save(self):
        docs = self._cache.values() + self._new
        if len(docs) > 0:
            inserted_docs = self._db.update(docs)
            for doc, newdoc in zip(docs, inserted_docs):
                if newdoc[0]:
                    doc["_id"], doc["_rev"] = newdoc[1], newdoc[2]
                    self.inserted += 1
            self._cache = {}
            self._new = []
```
