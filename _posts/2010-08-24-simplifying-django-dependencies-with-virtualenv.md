---
layout: post
title: Simplifying Django dependencies with virtualenv
date: 2010-08-24 13:23:49.000000000 +01:00
tags:
- dependency
- django
- python
- virtualenv
- deployment
permalink: "/2010/08/24/simplifying-django-dependencies-with-virtualenv/"
flickr_user: 'http://www.flickr.com/photos/austinevan/'
flickr_username: "Evan Bench"
flickr_image: 'https://live.staticflickr.com/1173/1225274637_85fac883b1_w.jpg'
flickr_imagelink: 'http://www.flickr.com/photos/austinevan/1225274637/'
flickr_imagename: "books in a stack (a stack of books)"
---
`virtualenv` is a tool for simplifying dependency management in Python applications. As the name
suggests, `virtualenv` creates a virtual environment which makes it easy to install Python packages
without needing root privileges to do so.

To use the packages installed in a virtual environment you run the `activate` script in the
`bin` directory of the virtual environment. This is fine when you're working on the command line, but
you don't want to have to remember this step when running the debug server, and it's hard to get that to work
when the site is deployed under `mod_wsgi`.

To make things easier you can add the appropriate directory from the virtual environment to Python's path as
part of `manage.py`, or the appropriate `fcgi` or `wsgi` control script.

```python
import os
import sys
import siten
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
site.addsitedir(os.path.join(root_dir, 've/lib/python%i.%i/site-packages'
                % (sys.version_info[0], sys.version_info[1])))
```

Just add the code above to the top of your `manage.py` file and the `ve` virtual environment
will always be activated when you run the script.
