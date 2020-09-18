---
layout: post
title: Placing Django Models In Separate Files
date: 2009-01-20 13:20:15
tags:
- django
- web development
permalink: "/2009/01/20/placing-django-models-in-separate-files/"
---
[Chris Petrilli](http://blog.amber.org/) has made a very useful post on [placing Django models into separate
files](http://blog.amber.org/2009/01/19/moving-django-models-into-their-own-module/).

The first thing I do when starting a Django project is to delete the standard views.py file and replace it
with a directory. It won't take you long before you've written enough views that a single file becomes huge.
The same is true of models.py. If you have ten or more models then the file can quickly become a thousand line
behemoth. I'd tried to split the file into a directory before, but it never worked, and the error messages
were never helpful.
<!--more-->

The solution is simple, you add a Meta class to your model with an app_label parameter.

```python
from django.db import models

class Test(models.Model):
    class Meta:
        app_label = 'myapp'
```

So, thanks Chris!
