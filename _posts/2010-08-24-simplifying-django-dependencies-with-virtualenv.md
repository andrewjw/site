---
layout: post
title: Simplifying Django dependencies with virtualenv
date: 2010-08-24 13:23:49.000000000 +01:00
type: post
parent_id: '0'
published: true
password: ''
status: publish
categories:
- deployment
tags:
- dependency
- django
- python
- virtualenv
meta:
  _edit_last: '364050'
  _wpas_done_twitter: '1'
  _wp_old_slug: ''
author:
  login: andrewjw
  email: andrewjwilkinson@gmail.com
  display_name: Andrew Wilkinson
  first_name: Andrew
  last_name: Wilkinson
permalink: "/2010/08/24/simplifying-django-dependencies-with-virtualenv/"
---
<a href="http://www.flickr.com/photos/austinevan/1225274637/"><img src="{{ site.baseurl }}/assets/1225274637_85fac883b1_m.jpg" alt="books in a stack (a stack of books) by austinevan" style="float:right;border:0;" /></a><a>virtualenv</a> is a tool for simplifying dependency management in Python applications. As the name suggests, <tt>virtualenv</tt> creates a virtual environment which makes it easy to install Python packages without needing root privileges to do so.n
To use the packages installed in a virtual environment you run the <tt>activate</tt> script in the <tt>bin</tt> directory of the virtual environment. This is fine when you're working on the command line, but you don't want to have to remember this step when running the debug server, and it's hard to get that to work when the site is deployed under <tt>mod_wsgi</tt>.n
To make things easier you can add the appropriate directory from the virtual environment to Python's path as part of <tt>manage.py</tt>, or the appropriate <tt>fcgi</tt> or <tt>wsgi</tt> control script.n
[code]<br />
import os<br />
import sys<br />
import siten
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))n
site.addsitedir(os.path.join(root_dir, 've/lib/python%i.%i/site-packages' % (sys.version_info[0], sys.version_info[1])))<br />
[/code]n
Just add the code above to the top of your <tt>manage.py</tt> file and the <tt>ve</tt> virtual environment will always be activated when you run the script.n
<hr />
Photo of <a href="http://www.flickr.com/photos/austinevan/1225274637/">books in a stack (a stack of books)</a> by <a href="http://www.flickr.com/photos/austinevan">austinevan</a>.n