---
layout: post
title: Continuous Integration Testing
date: 2010-06-30 14:16:27.000000000 +01:00
type: post
tags:
- deployment
- buildbot
- django
- python
- testing
permalink: "/2010/06/30/continuous-integration-testing/"
flickr_user: 'https://www.flickr.com/photos/mythoto/'
flickr_username: "Leonard J Matthews"
flickr_image: 'https://live.staticflickr.com/3036/2917647893_e04eba796c_w.jpg'
flickr_imagelink: 'https://www.flickr.com/photos/mythoto/2917647893/'
flickr_imagename: "from whence the brick came"
---
At work we recently set up [Buildbot](http://buildbot.net/) to replace an in-house continuous
integration tool that never really took off.  I've used Buildbot before, in a hobby capacity, but using it my
day job has really brought home to me how important not only testing is, but testing continuously.

Buildbot is pretty simple to explain. Every time you make a commit to your source control system this triggers
buildbot to run a series of steps over your code. What these steps are is totally configurable by you.
Typically though, you'll configure it to check out your code, compile it and run unit tests.

I'm a big fan of test driven and issue driven development. With these two methodologies when you want to make
a change you record the issue in your bug tracking software, then write a test that detects the deficiency in
your code. Once you've done that you can start actually making the change that you wanted to make in the first
place.  By writing down the issue you're forced into thinking about the change that you want to make, and
creating the test ensures that you know when it's complete.

TDD and IDD are useful things to aim for, but in reality you'll probably fall short sometimes. Not everything
can be unit tested easily, or you might be under significant time pressures that force you to cut corners.
One of the projects I manage has a test suite that takes 25 minutes to run. If I'm getting phone calls urging
me to fix a problem as soon as possible then I can't wait for the tests to run before I commit the change.

Because builtbot runs without user intervention you don't need to remember to do anything. Buildbot is also a
nag. If you introduce a bug with a change you quickly get an email letting you know that there is a problem,
and if you set those emails up to go to your team then you also have peer pressure to get that problem fixed.

I spend most of my time building [Django](http://www.djangoproject.com) based sites. For these
sites I set up six steps for Buildbot to follow. The first step is the checkout step, then a step to copy a settings file into place. Django stores settings in a Python file and these settings need to be configured
for each server that the site is run on. I typically have a file `settings_local.py.buildbot` stored
in the repository and this step copies this file to `settings_local.py` so the following commands will
run with the correct settings. The next step is to download and install the dependencies of the site. I'm
going to go into more detail on how I manage settings and dependencies in a future post, but Buildbot just
runs the correct commands.

The first three steps that Buildbot runs are just configuration steps. The first of the real test is a simple
compilation step. It's rare that a change gets committed without it ever being run, but it's still worthwhile
to check that the code compiles. It is possible that when merging changes from different branches errors can
creep in. Fortunately Python makes it easy to check that all the files in a directory structure compile using
the `compileall` module. This can be run using the command `python -m compileall -q` which
return an exit code of zero if all the files compile, and nonzero if there is an error. This means that if
there is an error Buildbot will detect it, and mark the build as failed.

The next step I run is the unit tests. This where the bulk of the testing occurs. I'm not going to go into
details on how to write unit tests, but assuming you have them this assures you that your tests pass after
every commit. Because Buildbot can be easily configured to build on several different machines on each commit
you can easily test that a change you made on a Python 2.5 machine also works on a Python 2.4 machine.

The final step I run is [PyLint](http://www.logilab.org/857). PyLint checks that your code complies
with a set of coding standards and simple checks. If your unit tests don't have a 100% coverage (and frankly,
whose does?) then PyLint will hep detect that there are no obvious flaws in your code. PyLint takes a bit of
time to configure, especially as it doesn't like some of the metaclass magic that Django uses, but once you
have a configuration file written PyLint is an excellent final check.

Hopefully this has given you a flavour of what Buildbot can do for you, and if you're in a team or are
building a cross-platform piece of software then Buildbot really needs to be there, watching your back.
