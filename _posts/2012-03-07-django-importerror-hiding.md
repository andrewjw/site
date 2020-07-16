---
layout: post
title: Django ImportError Hiding
date: 2012-03-07 13:59:29.000000000 +00:00
type: post
parent_id: '0'
published: true
password: ''
status: publish
categories:
- web development
tags:
- django
- error handling
- exceptions
- python
meta:
  _edit_last: '364050'
  publicize_results: a:1:{s:7:"twitter";a:1:{i:5934552;a:2:{s:7:"user_id";s:10:"andrew_j_w";s:7:"post_id";s:18:"177393044478373889";}}}
  _wpas_done_twitter: '1'
author:
  login: andrewjw
  email: andrewjwilkinson@gmail.com
  display_name: Andrew Wilkinson
  first_name: Andrew
  last_name: Wilkinson
permalink: "/2012/03/07/django-importerror-hiding/"
---
<a href="http://www.flickr.com/photos/grahford/458564891/"><img style="float:right;border:0;" src="{{ site.baseurl }}/assets/458564891_5e943e5794_m.jpg" alt="Hidden Cat" /></a>A little while ago I was asked what my biggest gripe with Django was. At the time I couldn't think of a good answer because since I started using Django in the pre-1.0 days most of the rough edges have been smoothed. Yesterday though, I encountered an error that made me wish I thought of it at the time.n
The code that produced the error looked like this:n
[code language="python"]<br />
from django.db import modelsn
class MyModel(model.Model):<br />
    ...n
    def save(self):<br />
        models.Model.save(self)n
        ...n
    ...<br />
[/code]n
The error that was raised was <tt>AttributeError: 'NoneType' object has no attribute 'Model'</tt>. This means that rather than containing a module object, <tt>models</tt> was None. Clearly this is impossible as the class could not have been created if that was the case. Impossible or not, it was clearly happening.n
Adding a print statement to the module showed that when it was imported the <tt>models</tt> variable did contain the expected module object. What that also showed was that module was being imported more than once, something that should also be impossible.n
After a wild goose chase investigating reasons why the module might be imported twice I tracked it down to the <tt>load_app</tt> method in <tt>django/db/models/loading.py</tt>. The code there looks something like this:n
[code language="python"]<br />
    def load_app(self, app_name, can_postpone=False):<br />
        try:<br />
            models = import_module('.models', app_name)<br />
        except ImportError:<br />
            # Ignore exception<br />
[/code]n
Now I'm being a harsh here, and the exception handler does contain a comment about working out if it should reraise the exception. The issue here is that it wasn't raising the exception, and it's really not clear why. It turns out that I had a misspelt module name in an import statement in a different module. This raised an <tt>ImportError</tt> which was caught, hidden and then Django repeatedly attempted to import the models as they were referenced in the models of other apps. The strange exception that was originally encountered is probably an artefact of Python's garbage collection, although how exactly it occurred is still not clear to me.n
There are a number of tickets (<a href="https://code.djangoproject.com/ticket/6379">#6379</a>, <a href="https://code.djangoproject.com/ticket/14130">#14130</a> and probably others) on this topic. A common refrain in Python is that it's easier to ask for forgiveness than to ask for permission, and I certainly agree with Django and follow that most of the time.n
I always follow the rule that try/except clauses should cover as little code as possible. Consider the following piece of code.n
[code language="python"]<br />
try:<br />
    var.method1()n
    var.member.method2()<br />
except AttributeError:<br />
    # handle error<br />
[/code]n
Which of the three attribute accesses are we actually trying to catch here? Handling exceptions like this are a useful way of implementing Duck Typing while following the easier to ask forgiveness principle. What this code doesn't make clear is which member or method is actually optional. A better way to write this would be:n
[code language="python"]<br />
var.method1()n
try:<br />
    member = var.member<br />
except AttributeError:<br />
    # handle error<br />
else:<br />
    member.method2()<br />
[/code]n
Now the code is very clear that the <tt>var</tt> variable may or may not have a <tt>member</tt> member variable. If <tt>method1</tt> or <tt>method2</tt> do not exist then the exception is not masked and is passed on. Now lets consider that we want to allow the <tt>method1</tt> attribute to be optional.n
[code language="python"]<br />
try:<br />
    var.method1()<br />
except AttributeError:<br />
    # handle error<br />
[/code]n
At first glance it's obvious that <tt>method1</tt> is optional, but actually we're catching too much here. If there is a bug in <tt>method1</tt> that causes an <tt>AttributeError</tt> to raised then this will be masked and the code will treat it as if <tt>method1</tt> didn't exist. A better piece of code would be:n
[code language="python"]<br />
try:<br />
    method = var.method1<br />
except AttributeError:<br />
    # handle error<br />
else:<br />
    method()<br />
[/code]n
<tt>ImportError</tt>s are similar because code can be executed, but then when an error occurs you can't tell whether the original import failed or whether an import inside that failed. Unlike with an <tt>AttributeError</tt> there is a no easy way to rewrite the code to only catch the error you're interested in. Python does provide some tools to divide the import process into steps, so you can tell whether the module exists before attempting to import it. In particular the <tt><a href="http://docs.python.org/library/imp.html#imp.find_module">imp.find_module</a></tt> function would be useful.n
Changing Django to avoid catching the wrong <tt>ImportError</tt>s will greatly complicate the code. It would also introduce the danger that the algorithm used would not match the one used by Python. So, what's the moral of this story? Never catch more exceptions than you intended to, and if you get some really odd errors in your Django site watch out for <tt>ImportErrors</tt>.n
<hr />
Photo of <a href="http://www.flickr.com/photos/grahford/458564891/">Hidden Cat</a> by <a href="http://www.flickr.com/photos/grahford/">Craig Grahford</a>.n
