---
layout: post
title: CouchDB Performance
date: 2008-09-19 12:17:31
tags: couchdb performance
permalink: "/2008/09/19/couchdb-performance/"
---
I've been toying with [CouchDB](http://couchdb.org/) for a short while, and I'm definitely
impressed by what I've seen. Once I'd upgraded to [Erlang](http://www.erlang.org/) R12B and
trunk CouchDB any bugs I was seeing disappearing and importing all 1 million documents was straightforward.

With 1 million documents the map/reduce takes a long time, as you would expect. What would be nice
is if the maps could be spread across different nodes to speed things up dramatically. Once the map
has been calculated and cached, retrieving it is relatively fast. Parsing it in Python does seem to
be quite slow, taking a few seconds for a few tens of thousands of results. This is far too slow for a webpage response.

Is there any way to speed up CouchDB? Well aggressive use of memcache will probably help, but too
me it seems that CouchDB is not suited to large datasets. I do hope I'm wrong though, and I'm going
to investigate further because I really want to find a use for CouchDB in my work.
