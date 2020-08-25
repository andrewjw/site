---
layout: post
title: CouchQL development progressing
date: 2009-04-30T11:14:54.000Z
tags:
  - couchdb
  - couchql
permalink: /2009/04/30/couchql-development-progressing/
---
As I mentioned in a [previous post](http://www.theandrewwilkinson.com/2009/04/16/introducing-couchql/) I have
been working of a library to ease the creation of map/reduce views in
[CouchDB](http://code.google.com/p/couchdb-python/).

The code is being hosted on [google code](http://code.google.com/p/couchql/) and can be checked out and used
now. The development is currently at a very early stage, but the fundamentals are sound.

Code such that given below will work. In this example it will return all the documents with a member 'x' whoes
value is greater than one.

```python
c = db.cursor()
c.execute("SELECT * FROM _ WHERE x > %s", (1, ))
for doc in c.fetchall():
    # process doc
```

The code is executed as a temporary view, but very high on my list is to use permanent views for much higher
performance. This will be added before a first release, as will the ability to have multiple expressions anded
together in the where clause.
