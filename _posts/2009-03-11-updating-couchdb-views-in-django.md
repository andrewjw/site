---
layout: post
title: Updating CouchDB Views In Django
date: 2009-03-11 13:24:36.000000000 +00:00
type: post
parent_id: '0'
published: true
password: ''
status: publish
categories:
- web development
tags:
- couchdb
- django
meta:
  _edit_last: '364050'
author:
  login: andrewjw
  email: andrewjwilkinson@gmail.com
  display_name: Andrew Wilkinson
  first_name: Andrew
  last_name: Wilkinson
permalink: "/2009/03/11/updating-couchdb-views-in-django/"
---
<a href="http://couchdb.apache.org/">CouchDB</a> views are a bit like stored procedures in a traditional database system. As with stored procedures it's difficult to keep them in sync with your code, and to keep them in your version control system. In this article I'll show you how you can use a <a href="http://andrewwilkinson.wordpress.com/2009/03/06/creating-django-management-commands/">django management command</a> to update your views from files in your code base.

CouchDB uses a map/reduce system where each view is made of a filter program (the map) and an optional post processor that runs over the output of the map (the reduce). These pairs are grouped into design documents which are stored as a single unit in the couchdb database.

This command assumes that you store your map and reduce functions in the directory structure set out below.n

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

Inside your app directory create a folder called <tt>couchviews</tt>. Inside that create one for each of your CouchDB databases. Finally, create two layers of directories to represent the design documents and views stored within. Each javascript file should contain a single anonymous function.

For this management command to work your settings file needs to contain a variable for each database, containing the Python CouchDB database objects. In this example three variables need to be added to <tt>ettings.py</tt> - <tt>database1</tt>, <tt>database2</tt> and <tt>database3</tt>.

Add the code below to the file <tt>project/app/mangement/commands/updatecouchviews.py</tt> and when you type <tt>manage.py updatecouchviews</tt> it'll walk your directory structure and update all your design documents in one fell swoop. Easy!

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