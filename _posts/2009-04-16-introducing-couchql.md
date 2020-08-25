---
layout: post
title: Introducing CouchQL
date: 2009-04-16T11:49:40.000Z
type: post
tags:
  - couchdb
  - couchql
  - databases
  - python
  - sql
permalink: /2009/04/16/introducing-couchql/
---
[CouchDB](http://couchdb.apache.org/) is a very exciting development in the world of databases and I'm greatly
enjoying building a website which uses it. One problem is that most of the of views that I have created are
extremely simple and could easily be represented using SQL. Although I [wrote some
code](/2009/03/11/updating-couchdb-views-in-django/) to help make life
easier, creating a view such as that below is never going to be as simple as including `SELECT * FROM table
WHERE (status="open" OR status="accepted") AND latest AND key="xyz"` directly in your code.

```javascript
function (doc) {
    if((doc["status"] == "open" || doc["status"] == "accepted") && doc["latest"]) {
        emit(doc["key"], null);
    }
}
```

The SQL above and the Javascript view function are directly equivalent, which is why I've started working on
an extension to the [Python CouchDB](http://code.google.com/p/couchdb-python/) library, which I've decided to
call [CouchQL](http://code.google.com/p/couchql/).

The basic strategy is going to be this. The library adds a method to the `Database` object, `cursor` which
returns an object which is compatible with the standard Python database API. When executing a CouchQL query a
hash is taken of the textual query and a call is made to the view `couchql_<i>hash</i>`. If the view is not
found then the query is turned into Javascript, added the server and the call repeated.

One of the common mistakes with CouchDB is to treat as if it were a traditional RDBMS. CouchQL has the danger
of confusing people even more by allowing users to query CouchDB as if it **is** an RDBMS. CouchQL is not
SQL, even if it does pretend to be SQL-like. I've not yet decided on how much processing should be done in the
library to make the query language more SQL-like. The query `SELECT * FROM table WHERE x > 5 OR x < 3` cannot
be directly represented as call to a CouchDB view. It can be represented as two separate calls to the same
view with the results merged. Is this a good idea? I'm not sure.

Development work has only just started on this library, but I'm actively working on and hope to be able to
announce something useful to the CouchDB mailing list soon.
