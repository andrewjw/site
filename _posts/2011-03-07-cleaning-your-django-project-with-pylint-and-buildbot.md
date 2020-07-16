---
layout: post
title: Cleaning Your Django Project With PyLint And Buildbot
date: 2011-03-07 13:39:23.000000000 +00:00
type: post
parent_id: '0'
published: true
password: ''
status: publish
categories:
- python
tags:
- buildbot
- code
- django
- programming
- pylint
meta:
  _edit_last: '364050'
  _wpas_done_twitter: '1'
author:
  login: andrewjw
  email: andrewjwilkinson@gmail.com
  display_name: Andrew Wilkinson
  first_name: Andrew
  last_name: Wilkinson
permalink: "/2011/03/07/cleaning-your-django-project-with-pylint-and-buildbot/"
---
<a href="http://www.flickr.com/photos/inf3ktion/4477642894/"><img src="{{ site.baseurl }}/assets/4477642894_2cfbc8ea4f_m.jpg" alt="Cleaning by inf3ktion" style="float:right;border:0;" /></a>There are a number of tools for checking whether your Python code meets a coding standard. These include <a href="http://pypi.python.org/pypi/pep8">pep8.py</a>, <a href="http://pychecker.sourceforge.net/">PyChecker</a> and <a href="http://www.logilab.org/857">PyLint</a>. Of these, PyLint is the most comprehensive and is the tool which I prefer to use as part of <a href="http://andrewwilkinson.wordpress.com/2010/06/30/continuous-integration-testing/">my buildbot checks</a> that run on every commit.n
PyLint works by parsing the Python source code itself and checking things like using variables that aren't defined, missing doc strings and a large array of other checks. A downside of PyLint's comprehensiveness is that it runs the risk of generating false positives. As it parses the source code itself it struggles with some of Python's more dynamic features, in particular <a href="http://www.voidspace.org.uk/python/articles/metaclasses.shtml">metaclasses</a>, which, unfortunately, are a key part of Django. In this post I'll go through the changes I make to the standard PyLint settings to make it more compatible with Django.n
[code]<br />
disable=W0403,W0232,E1101<br />
[/code]n
This line disables a few problems that are picked up entirely. <tt>W0403</tt> stops relative imports from generating a warning, whether you want to disable these or not is really a matter of personal preference. Although I appreciate why there is a check for this, I think this is a bit too picky. <tt>W0232</tt> stops a warning appearing when a class has no <tt>__init__</tt> method. Django models will produce this warning, but because they're metaclasses there is nothing wrong with them. Finally, <tt>E1101</tt> is generated if you access a member variable that doesn't exist. Accessing members such as <tt>id</tt> or <tt>objects</tt> on a model will trigger this, so it's simplest just to disable the check.n
[code]<br />
output-format=parseable<br />
include-ids=yes<br />
[/code]n
These makes the output of PyLint easier to parse by Buildbot, if you're not using it then you probably don't need to include these lines.n
[code]<br />
good-names= ...,qs<br />
[/code]n
Apart from a limited number of names PyLint tries to enforce a minimum size of three characters in a variable name. As <tt>qs</tt> is such a useful variable name for a QuerySet I force this be allowed as a good name.n
[code]<br />
max-line-length=160<br />
[/code]n
The last change I make is to allow much longer lines. By default PyLint only allows 80 character long lines, but how many people have screens that narrow anymore? Even the argument that it allows you to have two files side by side doesn't hold water in this age where multiple monitors for developers are the norm.n
PyLint uses the exit code to indicate what errors occurred during the run. This confuses Buildbot which assumes that a non-zero return code means the program failed to run, even when using the <a href="http://buildbot.net/buildbot/docs/0.8.0/PyLint.html">PyLint buildstep</a>. To work around this I use a simple management command to duplicate the <tt>pylint</tt> program's functionality but that doesn't let the return code propagate back to Builtbot.n
[code lang="python"]<br />
from django.core.management.base import BaseCommandn
from pylint import lintn
class Command(BaseCommand):<br />
    def handle(self, *args, **options):<br />
        lint.Run(list(args + (&quot;--rcfile=../pylint.cfg&quot;, )), exit=False)<br />
[/code]n
<hr />
Photo of <a href="http://www.flickr.com/photos/inf3ktion/4477642894/">Cleaning</a> by <a href="http://www.flickr.com/photos/inf3ktion">inf3ktion</a>.n
