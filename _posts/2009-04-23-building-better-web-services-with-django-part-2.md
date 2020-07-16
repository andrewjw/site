---
layout: post
title: Building Better Web Services With Django (Part 2)
date: 2009-04-23 12:28:00.000000000 +01:00
type: post
parent_id: '0'
published: true
password: ''
status: publish
categories:
- web development
tags:
- content type
- django
- headers
- http
- rest
- restful
- web services
meta:
  _edit_last: '364050'
author:
  login: andrewjw
  email: andrewjwilkinson@gmail.com
  display_name: Andrew Wilkinson
  first_name: Andrew
  last_name: Wilkinson
permalink: "/2009/04/23/building-better-web-services-with-django-part-2/"
---
In the <a href="http://andrewwilkinson.wordpress.com/2009/04/08/building-better-web-services-with-django-part-1/">first part</a> I talked about using the <tt>Content-Type</tt> and <tt>Accept</tt> HTTP headers to allow a single website to be use both by humans and programs.n
In the previous part I gave a decorator which can be used to make working with JSON very easy. For our use though this isn't great because a view decorated in this way only accepts JSON as the POST body and only returns JSON, regardless of the HTTP headers.n
The decorator given below relies on a <a href="http://www.djangosnippets.org/snippets/1042/">django snippet</a> to decode the <tt>Accept</tt> header for us so don't forget to added it to your middleware.n
<pre>
def content_type(func, common=None, json_in=None, json_out=None, form_in=None):
    def wrapper(req, *args, **kwargs):
        # run the common function, if we have one
        if common is not None:
            args, kwargs = common(req, *args, *kwargs), {}
            if isinstance(args, HttpResponse): return args
        content_type = req.META.get("content_type", "")
        if content_type == "application/json":
            args, kwargs = json_in(req, json.loads(req.raw_post_data), *args, *kwargs), {}
        elif content_type == "application/x-www-form-urlencoded":
            args, kwargs = json_in(req, req.POST, *args, *kwargs), {}
        else:
             return HttpResponse(status=415, "Unsupported Media Type")

        if isinstance(args, HttpResponse): return args

        for (media_type, q_value) in req.accepted_types:
            if media_type == "text/html":
                return func(req, args, kwargs)
            else:
                r = json_out(req, args, kwargs)
                if isinstance(r, HttpResponse):
                    return r
                else:
                    return HttpResponse(json.dumps(r), mimetype="application/json")
         return func(req, args, kwargs)
    return wrapper
</pre>
So, how can we use this decorator? Let's imagine we're creating a blog and we have a view which displays a post on that blog. If they user posts it should create a new comment. Firstly we create a function, <tt>common</tt>, which gets the blog object and returns a 404 if it doesn't exist. The return of this function is passed onto all other functions as their arguments.n
<pre>
def common(req, blog_id):
    try:
        return (get_post_by_id(int(blog_id)), )
    except ValueError:
        return HttpResponse(status=404)
</pre>
Next we write two functions to handle the cases where the users POSTs a form encoded body, or some JSON. The return values of these functions are passed onto the chosen output function as the arguments.n
<pre>
def json_in(req, json, blog_post):
    # process json
    return (blog_post ,)

def form_in(req, form, blog_post):
    # process form
    return (blog_post, )
</pre>
The JSON output function doesn't need to return an HttpResponse object like a normal Django view because the output is automatically encoded as a string and wrapped in a response object.n
<pre>
def json_out(req, blog_post):
    return blog_post.to_json()
</pre>
Finally we come to the HTML output function. This function is also called if not mime type in <tt>Accept</tt> is suitable.n
<pre>
@content_type(common=common, json_in=json_in, json_out=json_out, form_in=form_in)
def blog_post(req, blog_post):
    return render_to_template("post.html", {"post": blog_post})
</pre>
This decorator is really little more than a sketch. Many more content types could be supported, but hopefully it gives a good example of how you can write a very flexible webservice and still reduce code duplication as much as possible.n
