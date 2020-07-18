---
layout: post
title: Integrating Python and Javascript with PyV8
date: 2012-01-23 14:15:51.000000000 +00:00
type: post
parent_id: '0'
published: true
password: ''
status: publish
categories:
- python
tags:
- google
- javascript
- pyv8
- v8
meta:
  _edit_last: '364050'
  publicize_results: a:1:{s:7:"twitter";a:1:{i:5934552;a:2:{s:7:"user_id";s:10:"andrew_j_w";s:7:"post_id";s:18:"161452089711673344";}}}
  _wpas_done_twitter: '1'
author:
  login: andrewjw
  email: andrewjwilkinson@gmail.com
  display_name: Andrew Wilkinson
  first_name: Andrew
  last_name: Wilkinson
permalink: "/2012/01/23/integrating-python-and-javascript-with-pyv8/"
---
<a href="http://www.flickr.com/photos/scania/2869106546/"><img style="float:right;border:0;" src="{{ site.baseurl }}/assets/2869106546_662f446a43_m.jpg" alt="Scania 500/560/580/620 hp 16-litre Euro 3/4/5 V8 engine" /></a>A hobby project of mine would be made much easier if I could run the same code on the server as I run in the web browser. Projects like <a href="http://nodejs.org/">Node.js</a> have made Javascript on the server a more realistic prospect, but I don't want to give up on <a href="http://www.python.org/">Python</a> and <a href="http://www.djangoproject.com/">Django</a>, my preferred web development tools.n
The obvious solution to this problem is to embed Javascript in Python and to call the key bits of Javascript code from Python. There are two major Javascript interpreters, <a href="https://developer.mozilla.org/en/SpiderMonkey">Mozilla's SpiderMonkey</a> and <a href="http://code.google.com/p/v8/">Google's V8</a>. Unfortunately the <a href="http://code.google.com/p/python-spidermonkey/">python-spidermonkey</a> project is dead and there's no way of telling if it works with later version of SpiderMonkey. The <a href="http://code.google.com/p/pyv8/updates/list">PyV8</a> project by contrast is still undergoing active development.n
Although PyV8 has a wiki page entitled <a href="http://code.google.com/p/pyv8/wiki/HowToBuild">How To Build</a> it's not simple to get the project built. They recommend using prebuilt packages, but there are none for recent version of Ubuntu. In this post I'll describe how to build it on Ubuntu 11.11 and give a simple example of it in action.n
The first step is make sure you have the appropriate packages. There may be others that are required and not part of the default install, but there are what I had to install.n
[code language="bash"]<br />
sudo aptitude install scons libboost-python-dev<br />
[/code]n
Next you need to checkout both the V8 and PyV8 projects using the commands below.n
[code language="bash"]<br />
svn checkout http://v8.googlecode.com/svn/trunk/ v8<br />
svn checkout http://pyv8.googlecode.com/svn/trunk/ pyv8<br />
[/code]n
The key step before building PyV8 is to set the <tt>V8_HOME</tt> environment variable to the directory where you checked out the V8 code. This allows PyV8 to patch V8 and build it as a static library rather than the default dynamic library. Once you've set that you can use the standard Python <tt>setup.py</tt> commands to build and install the library.n
[code language="bash"]<br />
cd v8<br />
export PyV8=`pwd`<br />
cd ../pyv8<br />
python setup.py build<br />
sudo python setup.py install<br />
[/code]n
In future I'll write more detailed posts about how to use PyV8, but let's start with a simple example. <a href="http://mustache.github.com/">Mustache</a> is a simple template language that is ideal when you want to create templates in Javascript. There's actually a <a href="https://github.com/defunkt/pystache">Python implementation</a> of Mustache, but let's pretend that it doesn't exist.n
To start import the <tt>PyV8</tt> library and create a <tt>JSContext</tt> object. These are equivalent to sub-interpreters so you have several instance of your Javascript code running at once.n
[code language="python"]<br />
&gt;&gt;&gt; import PyV8<br />
&gt;&gt;&gt; ctxt = PyV8.JSContext()<br />
[/code]n
Before you can run any Javascript code you need <tt>enter()</tt> the context. You should also <tt>exit()</tt> it when you are complete. <tt>JSContext</tt> objects can be used with <tt>with</tt> statements to automate this, but for a console session it's simplest to call the method explicitly. Next we call <tt>eval()</tt> to run our Javascript code, first by reading in the Mustache library and then to set up our template as a variable.n
[code language="python"]<br />
&gt;&gt;&gt; ctxt.enter()<br />
&gt;&gt;&gt; ctxt.eval(open(&quot;mustache.js&quot;).read())<br />
&gt;&gt;&gt; ctxt.eval(&quot;var template = 'Javascript in Python is {{ opinion }}';&quot;)<br />
[/code]n
The final stage is to render the template by dynamically created some Javascript code. The results of the expressions are returned as Python objects, so here <tt>rendered</tt> contains a Python string.n
[code language="python"]<br />
&gt;&gt;&gt; import random<br />
&gt;&gt;&gt; opinion = random.choice([&quot;cool&quot;, &quot;great&quot;, &quot;nice&quot;, &quot;insane&quot;])<br />
&gt;&gt;&gt; rendered = ctxt.eval(&quot;Mustache.to_html(template, { opinion: '%s' })&quot; % (opinion, ))<br />
&gt;&gt;&gt; print rendered<br />
Javascript in Python is nice<br />
[/code]n
There's much more to PyV8 than I've described in this post, including calling Python code from Javascript but unfortunately the V8 and PyV8 documentation is a bit lacking. I will post some more of my discoveries in future posts.n
<hr />
Photo of <a href="http://www.flickr.com/photos/scania/2869106546/">Scania 500/560/580/620 hp 16-litre Euro 3/4/5 V8 engine</a> by <a href="http://www.flickr.com/photos/scania/">Scania Group</a>.n