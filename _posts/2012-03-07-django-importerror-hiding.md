---
layout: post
title: Django ImportError Hiding
date: 2012-03-07 13:59:29.000000000 +00:00
tags:
- django
- error handling
- exceptions
- python
- web development
permalink: "/2012/03/07/django-importerror-hiding/"
flickr_user: 'https://www.flickr.com/photos/grahford/'
flickr_username: "Jaron"
flickr_image: 'https://live.staticflickr.com/183/458564891_5e943e5794_w.jpg'
flickr_imagelink: 'https://www.flickr.com/photos/grahford/458564891/'
flickr_imagename: 'Hidden Cat'
---
A little while ago I was asked what my biggest gripe with Django was. At the time I couldn't think of a good
answer because since I started using Django in the pre-1.0 days most of the rough edges have been smoothed.
Yesterday though, I encountered an error that made me wish I thought of it at the time.

The code that produced the error looked like this:

```python
from django.db import models
class MyModel(model.Model):
    ...
    def save(self):
        models.Model.save(self)
        ...
    ...
```

The error that was raised was `AttributeError: 'NoneType' object has no attribute 'Model'`. This means
that rather than containing a module object, `models` was None. Clearly this is impossible as the class
could not have been created if that was the case. Impossible or not, it was clearly happening.
<!--more-->

Adding a print statement to the module showed that when it was imported the `models` variable did
contain the expected module object. What that also showed was that module was being imported more than once,
something that should also be impossible.

After a wild goose chase investigating reasons why the module might be imported twice I tracked it down to the
`load_app` method in `django/db/models/loading.py`. The code there looks something like this:

```python
    def load_app(self, app_name, can_postpone=False):
        try:
            models = import_module('.models', app_name)
        except ImportError:
            # Ignore exception
```

Now I'm being a harsh here, and the exception handler does contain a comment about working out if it should
reraise the exception. The issue here is that it wasn't raising the exception, and it's really not clear why.
It turns out that I had a misspelt module name in an import statement in a different module. This raised an
`ImportError` which was caught, hidden and then Django repeatedly attempted to import the models as
they were referenced in the models of other apps. The strange exception that was originally encountered is
probably an artefact of Python's garbage collection, although how exactly it occurred is still not clear to
me.

There are a number of tickets ([#6379](https://code.djangoproject.com/ticket/6379),
[#14130](https://code.djangoproject.com/ticket/14130) and probably others) on this topic. A common
refrain in Python is that it's easier to ask for forgiveness than to ask for permission, and I certainly agree
with Django and follow that most of the time.

I always follow the rule that try/except clauses should cover as little code as possible. Consider the
following piece of code.

```python
try:
    var.method1()n
    var.member.method2()
except AttributeError:
    # handle error
```

Which of the three attribute accesses are we actually trying to catch here? Handling exceptions like this
are a useful way of implementing Duck Typing while following the easier to ask forgiveness principle. What
this code doesn't make clear is which member or method is actually optional. A better way to write this would
be:

```python
var.method1()
try:
    member = var.member
except AttributeError:
    # handle error
else:
    member.method2()
```

Now the code is very clear that the `var` variable may or may not have a `member` member
variable. If `method1` or `method2` do not exist then the exception is not masked and is passed
on. Now lets consider that we want to allow the `method1` attribute to be optional.

```python
try:
    var.method1()
except AttributeError:
    # handle error
```

At first glance it's obvious that `method1` is optional, but actually we're catching too much here. If
there is a bug in `method1` that causes an `AttributeError` to raised then this will be masked
and the code will treat it as if `method1` didn't exist. A better piece of code would be:

```python
try:
    method = var.method1
except AttributeError:
    # handle error
else:
    method()
```

`ImportError`s are similar because code can be executed, but then when an error occurs you can't tell
whether the original import failed or whether an import inside that failed. Unlike with an
`AttributeError` there is a no easy way to rewrite the code to only catch the error you're interested
in. Python does provide some tools to divide the import process into steps, so you can tell whether the module
exists before attempting to import it. In particular the `
[imp.find_module](http://docs.python.org/library/imp.html#imp.find_module)` function would be
useful.

Changing Django to avoid catching the wrong `ImportError`s will greatly complicate the code. It would
also introduce the danger that the algorithm used would not match the one used by Python. So, what's the moral
of this story? Never catch more exceptions than you intended to, and if you get some really odd errors in your
Django site watch out for `ImportErrors`.
