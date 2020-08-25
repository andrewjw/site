---
layout: post
title: Cleaning Your Django Project With PyLint And Buildbot
date: 2011-03-07 14:04:09.000000000 +01:00
tags:
  - python
  - buildbot
  - code
  - django
  - programming
  - pylint
permalink: /2011/03/07/cleaning-your-django-project-with-pylint-and-buildbot/
flickr_user: 'https://www.flickr.com/photos/inf3ktion/'
flickr_username: "Roosh Inf3ktion"
flickr_image: 'https://live.staticflickr.com/4048/4477642894_2cfbc8ea4f_w.jpg'
flickr_imagelink: 'https://www.flickr.com/photos/inf3ktion/4477642894/'
flickr_imagename: 'Cleaning'
---
There are a number of tools for checking whether your Python code meets a coding standard. These include
[pep8.py](http://pypi.python.org/pypi/pep8), [PyChecker](http://pychecker.sourceforge.net/)
and [PyLint](http://www.logilab.org/857). Of these, PyLint is the most comprehensive and is the
tool which I prefer to use as part of
[my buildbot checks](/2010/06/30/continuous-integration-testing/)
that run on every commit.

PyLint works by parsing the Python source code itself and checking things like using variables that aren't
defined, missing doc strings and a large array of other checks. A downside of PyLint's comprehensiveness is
that it runs the risk of generating false positives. As it parses the source code itself it struggles with
some of Python's more dynamic features, in particular
[metaclasses](http://www.voidspace.org.uk/python/articles/metaclasses.shtml), which, unfortunately,
are a key part of Django. In this post I'll go through the changes I make to the standard PyLint settings to
make it more compatible with Django.

> disable=W0403,W0232,E1101

This line disables a few problems that are picked up entirely. `W0403` stops relative imports from
generating a warning, whether you want to disable these or not is really a matter of personal preference.
Although I appreciate why there is a check for this, I think this is a bit too picky. `W0232` stops a
warning appearing when a class has no `__init__` method. Django models will produce this warning, but
because they're metaclasses there is nothing wrong with them. Finally, `E1101` is generated if you
access a member variable that doesn't exist. Accessing members such as `id` or `objects` on a
model will trigger this, so it's simplest just to disable the check.

> output-format=parseable include-ids=yes

These makes the output of PyLint easier to parse by Buildbot, if you're not using it then you probably don't
need to include these lines.

> good-names= ...,qs

Apart from a limited number of names PyLint tries to enforce a minimum size of three characters in a variable
name. As `qs` is such a useful variable name for a QuerySet I force this be allowed as a good name.

> max-line-length=160

The last change I make is to allow much longer lines. By default PyLint only allows 80 character long lines,
but how many people have screens that narrow anymore? Even the argument that it allows you to have two files
side by side doesn't hold water in this age where multiple monitors for developers are the norm.

PyLint uses the exit code to indicate what errors occurred during the run. This confuses Buildbot which
assumes that a non-zero return code means the program failed to run, even when using the
[PyLint buildstep](http://buildbot.net/buildbot/docs/0.8.0/PyLint.html). To work around this I use a
simple management command to duplicate the `pylint` program's functionality but that doesn't let the
return code propagate back to Builtbot.

```python
from django.core.management.base import BaseCommand
from pylint import lint

class Command(BaseCommand):
    def handle(self, *args, **options):
        lint.Run(list(args + ("--rcfile=../pylint.cfg", )), exit=False)
```
