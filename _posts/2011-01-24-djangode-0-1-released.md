---
layout: post
title: DjangoDE 0.1 Released
date: 2011-01-24 14:04:09.000000000 +01:00
type: post
parent_id: '0'
published: true
status: publish
categories: []
tags:
  - django
  - djangode
  - editor
  - ide
  - programming
meta:
  _edit_last: '364050'
  _wpas_done_twitter: '1'
author:
  login: andrewjw
  email: andrewjwilkinson@gmail.com
  display_name: Andrew Wilkinson
  first_name: Andrew
  last_name: Wilkinson
permalink: /2011/01/24/djangode-0-1-released/
---
<a href="http://www.flickr.com/photos/romyboxsem/3270076250/"><img src="{{ site.baseurl }}/assets/3270076250_3272025421_m.jpg" alt="Op de laptop by romyboxsem" style="float:right;border:0;" /></a>I spend most of time at work building websites in <a href="http://www.djangoproject.com">Django</a>. My editor of choice until now has been <a href="http://kate-editor.org/">Kate</a> with <a href="http://www.chromium.org/Home">Chromium</a> open on another screen. Most of my co-workers use <a href="http://www.vim.org/">VIM</a> inside a <a href="http://www.chiark.greenend.org.uk/~sgtatham/putty/">PuTTY</a> session to do their editing. With multicore machines with gigabytes of RAM, surely there's a better way?

I investigated the current state of Django IDEs and came to conclusion that none of them are that great. Most are a plugin to a giant IDE that tries accommodate many different languages, so each feels like second best, or they are designed more for traditionally programming and not webdevelopment so they don't integrate with Django's in built server and don't support editing Javascript, or provide a built in webbrowser. I also don't want to have to pay for the editor, which limits my choice even more.

Having decided that none of the existing IDEs quite fit my requirements I did what any self respecting open source programmer with an itch would do, I headed to <a href="http://code.google.com/p">Google Code</a>, created a new project and then got coding.n
[caption id="" align="alignleft" width="300" caption="DjangoDE Main Editor Window"]<a href="http://code.google.com/p/djangode/"><img alt="" src="{{ site.baseurl }}/assets/main_window.png" title="DjangoDE Main Editor Window" width="300" /></a>[/caption]n
The project has now reached the stage where I feel I can make my first release, although this is a release that is very much in the spirit of the open source mantra, "release early, release often." The key features are all in place, which I'll talk about below, but they're all extremely basic and it's not ready to be used as a day-to-day editor. If you're looking for a Visual Studio replacement, this is not it.

The source can be downloaded from <a href="http://code.google.com/p/djangode/downloads/list">the project site</a>, or <a href="http://pypi.python.org/pypi/DjangoDE/0.1">PyPI</a>. The simplest method is just to run <tt>sudo easy_install djangode</tt>. You'll need to have <a href="http://www.riverbankcomputing.co.uk/software/pyqt/intro">PyQt</a> and of course Django installed. This first release also requires Linux, but being a Qt application that requirement will not exist for ever and it will eventually work on Windows (and hopefully Macs too).n
DjangoDE uses the <tt>manage.py</tt> file to define the scope of the project. The "Project" menu bar lets you pick a <tt>manage.py</tt> file to load, or to create a new Django project.n
The editor has a partial syntax highlighter for Python code implemented, and a quick access bar on the left of the window which lets you jump straight to the view implementing a particular url. It also has a tab for each application that is active in your project which lists the models.n
When you open DjangoDE it'll show you the <a href="http://www.djangoproject.com">Django project website</a> in a tab. If you  enter "/" into the address bar it'll load the front page of your website.

Pressing <tt>F9</tt> while viewing a source code file will create a breakpoint. If you then use the browser to view a page that passes that line the code will break and that point and the debug bar will appear. This shows you the variables in the current scope.

It's very early days for this project, but these features will be fleshed out in the coming releases. I'd like to encourage people to post <a href="http://code.google.com/p/djangode/issues/list">issues</a> if they come across bugs or want features implemented. You can also contact me through Twitter as <a href="http://www.twitter.com/djangoide"><tt>djangoide</tt></a>.
<hr />
Photo of <a href="http://www.flickr.com/photos/romyboxsem/3270076250/">Op de laptop</a> by <a href="http://www.flickr.com/photos/romyboxsem/">romyboxsem</a>.
