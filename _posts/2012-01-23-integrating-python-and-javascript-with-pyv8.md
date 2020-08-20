---
layout: post
title: Integrating Python and Javascript with PyV8
date: 2012-01-23 14:15:51.000000000 +00:00
tags:
- google
- javascript
- pyv8
- v8
- python
permalink: "/2012/01/23/integrating-python-and-javascript-with-pyv8/"
flickr_user: 'https://www.flickr.com/photos/robert_glod/'
flickr_username: "Robert GLOD"
flickr_image: 'https://live.staticflickr.com/65535/49820845412_c29f3b1a1a_w.jpg'
flickr_imagelink: 'https://www.flickr.com/photos/robert_glod/49820845412/'
flickr_imagename: 'Lasauvage History Vehicles - Ford GT40 V8 Engine'
---
A hobby project of mine would be made much easier if I could run the same code on the server as I run in the
web browser. Projects like [Node.js](http://nodejs.org/) have made Javascript on the server a more
realistic prospect, but I don't want to give up on [Python](http://www.python.org/) and <a
href="http://www.djangoproject.com/">Django</a>, my preferred web development tools.

The obvious solution to this problem is to embed Javascript in Python and to call the key bits of Javascript
code from Python. There are two major Javascript interpreters, <a
href="https://developer.mozilla.org/en/SpiderMonkey">Mozilla's SpiderMonkey</a> and <a
href="http://code.google.com/p/v8/">Google's V8</a>.

Unfortunately the [python-spidermonkey](http://code.google.com/p/python-spidermonkey/) project is
dead and there's no way of telling if it works with later version of SpiderMonkey. The <a
href="http://code.google.com/p/pyv8/updates/list">PyV8</a> project by contrast is still undergoing active
development.

Although PyV8 has a wiki page entitled [How To
Build](http://code.google.com/p/pyv8/wiki/HowToBuild) it's not simple to get the project built. They recommend using prebuilt packages, but there are none
for recent version of Ubuntu. In this post I'll describe how to build it on Ubuntu 11.11 and give a simple
example of it in action.

The first step is make sure you have the appropriate packages. There may be others that are required and not
part of the default install, but there are what I had to install.

```bash
sudo aptitude install scons libboost-python-dev
```

Next you need to checkout both the V8 and PyV8 projects using the commands below.

```bash
svn checkout http://v8.googlecode.com/svn/trunk/ v8
svn checkout http://pyv8.googlecode.com/svn/trunk/ pyv8
```

The key step before building PyV8 is to set the `V8_HOME` environment variable to the directory where
you checked out the V8 code. This allows PyV8 to patch V8 and build it as a static library rather than the
default dynamic library. Once you've set that you can use the standard Python `setup.py` commands to
build and install the library.

```bash
cd v8
export PyV8=`pwd`
cd ../pyv8
python setup.py build
sudo python setup.py install
```

In future I'll write more detailed posts about how to use PyV8, but let's start with a simple example. <a
href="http://mustache.github.com/">Mustache</a> is a simple template language that is ideal when you want to
create templates in Javascript. There's actually a [Python
implementation](https://github.com/defunkt/pystache) of Mustache, but let's pretend that it doesn't exist.

To start import the `PyV8` library and create a `JSContext` object. These are equivalent to
sub-interpreters so you have several instance of your Javascript code running at once.

```python
>>> import PyV8
>>> ctxt = PyV8.JSContext()
```

Before you can run any Javascript code you need `enter()` the context. You should also `exit()`
it when you are complete. `JSContext` objects can be used with `with` statements to automate
this, but for a console session it's simplest to call the method explicitly. Next we call `eval()` to
run our Javascript code, first by reading in the Mustache library and then to set up our template as a
variable.

```python
>>> ctxt.enter()
>>> ctxt.eval(open("mustache.js").read())
>>> ctxt.eval("var template = 'Javascript in Python is {{ opinion }}';")
```

The final stage is to render the template by dynamically created some Javascript code. The results of the
expressions are returned as Python objects, so here `rendered` contains a Python string.

```python
>>> import random
>>> opinion = random.choice(["cool", "great", "nice", "insane"])
>>> rendered = ctxt.eval("Mustache.to_html(template, { opinion: '%s' })" % (opinion, ))
>>> print rendered
Javascript in Python is nice
```

There's much more to PyV8 than I've described in this post, including calling Python code from Javascript but
unfortunately the V8 and PyV8 documentation is a bit lacking. I will post some more of my discoveries in
future posts.
