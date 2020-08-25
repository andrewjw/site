---
layout: post
title: "Creating Django Management Commands"
date: 2009-03-06 13:32:51.000000000 +00:00
tags:
- admin
- django
- tool
- web development
permalink: "/2009/03/06/creating-django-management-commands/"
---
Creating a website with Django is great fun, but eventually you'll need to write a tool to clean up you data,
expire old users or one of the myriad of other administration tasks that are involved with running a website.

You'll be very used to using manage.py to create your database and to run your webserver. It make sense to use
the same script for your own admin tools. Not only to get the benefit of sharing lots of you code but also
Django will take care of parsing command line arguments and importing your settings for you.

Unfortunately the [Django documentation](
http://docs.djangoproject.com/en/dev/howto/custom-management-commands/#howto-custom-management-commands) is
quite lacking on how to add your own command, but it's really quite easy.

If your app is in `project/app` then create the directories `project/app/management/commands`. Create an empty
file called `__init__.py` in both the `management` and `commands` directories. Once you've done that every
other python file in the commands directory can be executed via `manage.py`. If you create the file
`project/app/management/commands/x.py` then it can be run as `manage.py x`.

Each file which contains a command must define a class called `Command` which derives from
`django.core.management.base.BaseCommand`. Rather than derive directly from `BaseCommand` you'll most likely
want to derive from `NoArgsCommand`, `LabelCommand` or `AppCommand`. First I'll explain how to make a command
when deriving from `BaseCommand` and then we'll look at the helper classes.

```python
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--long', '-l', dest='long',
            help='Help for the long options'),
    )
    help = 'Help text goes here'

    def handle(self, **options):
        print "This is a command"
```

The code above should be fairly self explanatory. The code for your command goes inside the handle function,
while the options that your command accepts go in the options_list variable above. In this example the code
accepts one option, long, which will be passed as a value in the options dictionary.

If you command doesn't need any options then you should derive from NoArgsCommand and override handle_noargs
rather than handle.

The other two types of commands are AppCommand and LabelCommand. These both take any number of arguments on
the commandline, but AppCommand checks that they are app names while LabelCommand passes them on unchanged.
You should override handle_app and handle_label rather than handle, and these functions will be called once
for each commandline argument with the argument as the first parameter to the function.

For more inspiration take a look at the
[default management commands](http://code.djangoproject.com/svn/django/trunk/django/core/management/commands/)

Next time I'll show how you can write a real command which will help you keep your views updated if you use
couchdb as a datastore.
