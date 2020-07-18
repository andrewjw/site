---
layout: post
title: Building Better Web Services With Django (Part 1)
date: 2009-04-08T11:21:03.000Z
type: post
tags:
  - web development
  - content type
  - django
  - headers
  - http
  - rest
  - restful
  - web services
permalink: /2009/04/08/building-better-web-services-with-django-part-1/
---
Building a RESTful webservice is pretty straight-forward with Django, but in many cases you want to have both a human readable website and a machine readable api. A lot of websites solve this problem by using www.x.com as the human site, an api.x.com as the machine site. They also will typically have different structures to support the different usecases.n
Unless your documentation is really excellent and the person writing the client to your service actually reads it building a client for the service is an error prone process. In an ideal world the developer would be able to browse the website and use the same urls in their client program. Fortunately HTTP has two headers which make it possible to do just that, <tt>Content-Type</tt> and <tt>Accept</tt>.

The <tt>Content-Type</tt> header describes the type of data that is included in the body of the HTTP request. Typically this will be values such as <tt>text/html</tt>, <tt>application/json</tt> or <tt>application/x-www-form-urlencoded</tt>. A content type is sent by the client when POSTing or PUTing data, and whenever the webserver includes some data in its response. The <tt>Accept</tt> header is sent by a client to specify what content types it can accept in the response. This header has a more complicated format that <tt>Content-Type</tt> because it can used to specify a number of different content types and to give a weighting to each.

When combined these two headers can be used to allow a normal user to browse the site and to allow a robot to make api calls on the same site, using the same urls. This makes it easier both for the creator of the programmer accessing your site and for you because you can easily share code between the site and your api.

I'm going to outline a decorator that will let write a webservice such as this, that will support HTML and JSON output, and JSON and form encoded data as inputs.n
First we'll create a decorator that parses any post data as JSON and passes it the view as the second parameter (after the request object). It will also JSON encode any return value that's not an HTTPResponse object.

    import simplejson as json

    from django.http import HttpResponse

    def json_view(func):
        def wrap(req, *args, **kwargs):
            try:
                j = json.loads(req.raw_post_data)
            except ValueError:
                j = None

            resp = func(req, j, *args, **kwargs)

            if isinstance(resp, HttpResponse):
                return resp

            return HttpResponse(json.dumps(resp), mimetype="application/json")

        return wrap

This decorator should be pretty easy follow, but here is an example to illustrate its use.n

    @json_view
    def view(req, json, arg1, arg2):
        obj = get_obj(arg1, arg2)
        if req.method == "POST" and json is not None:
            # process json here
            return {"status": "ok"}
        else:
            return {"status": "failed"}

This really cuts down on the code you need to write, but this view only handles JSON as its input and output. Next we need to parse the <tt>Accept</tt> headers and return an ordered list of content types so we can choose the preferred option. No need to reinvent the wheel, so we just pull some code from <a href="http://www.djangosnippets.org/snippets/1042/">djangosnippets.org</a>.

All the parts are in place now, and in my next post we'll create a decorator which takes these parts ands puts them together.
