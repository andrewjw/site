---
layout: post
title: DjangoDE 0.1 Released
date: 2011-01-24 14:04:09.000000000 +01:00
type: post
tags:
  - django
  - djangode
  - editor
  - ide
  - programming
permalink: /2011/01/24/djangode-0-1-released/
flickr_user: 'https://www.flickr.com/photos/acnatta/'
flickr_username: "André Natta"
flickr_image: 'https://live.staticflickr.com/2496/4047061590_81b94f22d1_w.jpg'
flickr_imagelink: 'https://www.flickr.com/photos/acnatta/4047061590/'
flickr_imagename: 'The new laptop from "back"'
---
I spend most of time at work building websites in [Django](http://www.djangoproject.com). My editor of choice
until now has been [Kate](http://kate-editor.org/) with [Chromium](http://www.chromium.org/Home) open on
another screen. Most of my co-workers use [VIM](http://www.vim.org/) inside a
[PuTTY](http://www.chiark.greenend.org.uk/~sgtatham/putty/) session to do their editing. With multicore
machines with gigabytes of RAM, surely there's a better way?

I investigated the current state of Django IDEs and came to conclusion that none of them are that great. Most
are a plugin to a giant IDE that tries accommodate many different languages, so each feels like second best,
or they are designed more for traditionally programming and not webdevelopment so they don't integrate with
Django's in built server and don't support editing Javascript, or provide a built in webbrowser. I also don't
want to have to pay for the editor, which limits my choice even more.

Having decided that none of the existing IDEs quite fit my requirements I did what any self respecting open
source programmer with an itch would do, I headed to [Google Code](http://code.google.com/p), created a new
project and then got coding.

![DjangoDE Main Editor Window](/assets/djangode_main_window.png)

The project has now reached the stage where I feel I can make my first release, although this is a release
that is very much in the spirit of the open source mantra, "release early, release often." The key features
are all in place, which I'll talk about below, but they're all extremely basic and it's not ready to be used
as a day-to-day editor. If you're looking for a Visual Studio replacement, this is not it.

The source can be downloaded from [the project site](http://code.google.com/p/djangode/downloads/list), or
[PyPI](http://pypi.python.org/pypi/DjangoDE/0.1). The simplest method is just to run `sudo easy_install
djangode`. You'll need to have [PyQt](http://www.riverbankcomputing.co.uk/software/pyqt/intro) and of course
Django installed. This first release also requires Linux, but being a Qt application that requirement will not
exist for ever and it will eventually work on Windows (and hopefully Macs too).n DjangoDE uses the `manage.py`
file to define the scope of the project. The "Project" menu bar lets you pick a `manage.py` file to load, or
to create a new Django project.n The editor has a partial syntax highlighter for Python code implemented, and
a quick access bar on the left of the window which lets you jump straight to the view implementing a
particular url. It also has a tab for each application that is active in your project which lists the models.n
When you open DjangoDE it'll show you the [Django project website](http://www.djangoproject.com) in a tab. If
you  enter "/" into the address bar it'll load the front page of your website.

Pressing `F9` while viewing a source code file will create a breakpoint. If you then use the browser to view a
page that passes that line the code will break and that point and the debug bar will appear. This shows you
the variables in the current scope.

It's very early days for this project, but these features will be fleshed out in the coming releases. I'd like
to encourage people to post [issues](http://code.google.com/p/djangode/issues/list) if they come across bugs
or want features implemented. You can also contact me through Twitter as
[`djangoide`](http://www.twitter.com/djangoide).
