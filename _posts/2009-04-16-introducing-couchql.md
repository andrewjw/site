---
layout: post
title: Introducing CouchQL
date: 2009-04-16T11:49:40.000Z
type: post
parent_id: '0'
published: true
status: publish
categories: []
tags:
  - couchdb
  - couchql
  - databases
  - python
  - sql
meta:
  _edit_last: '364050'
author:
  login: andrewjw
  email: andrewjwilkinson@gmail.com
  display_name: Andrew Wilkinson
  first_name: Andrew
  last_name: Wilkinson
permalink: /2009/04/16/introducing-couchql/
---
<a href="http://couchdb.apache.org/">CouchDB</a> is a very exciting development in the world of databases and I'm greatly enjoying building a website which uses it. One problem is that most of the of views that I have created are extremely simple and could easily be represented using SQL. Although I <a href="https://www.theandrewwilkinson.com/2009/03/11/updating-couchdb-views-in-django/">wrote some code</a> to help make life easier, creating a view such as that below is never going to be as simple as including <tt>SELECT * FROM table WHERE (status="open" OR status="accepted") AND latest AND key="xyz"</tt> directly in your code.


    function (doc) {
        if((doc["status"] == "open" || doc["status"] == "accepted") &amp;&amp; doc["latest"]) {
            emit(doc["key"], null);
        }
    }

The SQL above and the Javascript view function are directly equivalent, which is why I've started working on an extension to the <a href="http://code.google.com/p/couchdb-python/">Python CouchDB</a> library, which I've decided to call <a href="http://code.google.com/p/couchql/">CouchQL</a>.

The basic strategy is going to be this. The library adds a method to the <tt>Database</tt> object, <tt>cursor</tt> which returns an object which is compatible with the standard Python database API. When executing a CouchQL query a hash is taken of the textual query and a call is made to the view <tt>couchql_<i>hash</i></tt>. If the view is not found then the query is turned into Javascript, added the server and the call repeated.

One of the common mistakes with CouchDB is to treat as if it were a traditional RDBMS. CouchQL has the danger of confusing people even more by allowing users to query CouchDB as if it <b>is</b> an RDBMS. CouchQL is not SQL, even if it does pretend to be SQL-like. I've not yet decided on how much processing should be done in the library to make the query language more SQL-like. The query <tt>SELECT * FROM table WHERE x &gt; 5 OR x &lt; 3</tt> cannot be directly represented as call to a CouchDB view. It can be represented as two separate calls to the same view with the results merged. Is this a good idea? I'm not sure.

Development work has only just started on this library, but I'm actively working on and hope to be able to announce something useful to the CouchDB mailing list soon.