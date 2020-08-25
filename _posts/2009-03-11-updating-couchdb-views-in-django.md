---
layout: post
title: Updating CouchDB Views In Django
date: 2009-03-11 13:24:36.000000000 +00:00
tags:
- web development
- couchdb
- django
permalink: "/2009/03/11/updating-couchdb-views-in-django/"
---
[CouchDB](http://couchdb.apache.org/) views are a bit like stored procedures in a traditional database system.
As with stored procedures it's difficult to keep them in sync with your code, and to keep them in your version
control system. In this article I'll show you how you can use a [django management
command](/2009/03/06/creating-django-management-commands/) to update your views from files in your code base.

CouchDB uses a map/reduce system where each view is made of a filter program (the map) and an optional post
processor that runs over the output of the map (the reduce). These pairs are grouped into design documents
which are stored as a single unit in the couchdb database.

This command assumes that you store your map and reduce functions in the directory structure set out below.

```plain
project/
    app/
        couchviews/
            database1/
                design1/
                    mapreduce1/
                        map.js reduce.js
                    mapreduce2/
                        map.js
                design2/
                    mapreduce3/
                        map.js reduce.js
             database3/
                 design3/
                     mapreduce4/
                         map.js reduce.js
```

Inside your app directory create a folder called `couchviews`. Inside that create one for each of your CouchDB
databases. Finally, create two layers of directories to represent the design documents and views stored
within. Each javascript file should contain a single anonymous function.

For this management command to work your settings file needs to contain a variable for each database,
containing the Python CouchDB database objects. In this example three variables need to be added to
`ettings.py` - `database1`, `database2` and `database3`.

Add the code below to the file `project/app/mangement/commands/updatecouchviews.py` and when you type
`manage.py updatecouchviews` it'll walk your directory structure and update all your design documents in one
fell swoop. Easy!

```python
import couchdb
import glob
import os

from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    help = "Update couchdb views"

    can_import_settings = True

    def handle_noargs(self, **options):
        import settings

        couchdir = os.path.realpath(os.path.split(__file__)[0] + "../../../couchviews")

        databases = glob.glob(couchdir+"/*")
        for d in databases:
            if not os.path.isdir(d):
                continue

            db = getattr(settings, d.split("/")[-1])

            for design in glob.glob(d + "/*"):
                design = design.split("/")[-1]
                try:
                    doc = db["_design/" + design]
                except couchdb.client.ResourceNotFound:
                    doc = {"_id": "_design/" + design}

                doc["views"] = {}
                for mapreduce in glob.glob(d+"/"+design+"/*"):
                    mapreduce = mapreduce.split("/")[-1]
                    mr = {}
                    mr["map"] = open(d+"/"+design+"/"+mapreduce+"/map.js").read()
                    try:
                        mr["reduce"] = reduce = open(d+"/"+design+"/"+mapreduce+"/reduce.js").read()
                    except IOError:
                        pass

                    doc["views"][mapreduce] = mr

                db["_design/" + design] = doc
```
