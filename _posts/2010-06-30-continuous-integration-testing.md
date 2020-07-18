---
layout: post
title: Continuous Integration Testing
date: 2010-06-30 14:16:27.000000000 +01:00
type: post
parent_id: '0'
published: true
password: ''
status: publish
categories:
- deployment
tags:
- buildbot
- django
- python
- testing
meta:
  _edit_last: '364050'
  _wp_old_slug: ''
  _wpas_done_twitter: '1'
  twitter_cards_summary_img_size: a:7:{i:0;i:240;i:1;i:178;i:2;i:2;i:3;s:24:"width="240"
    height="178"";s:4:"bits";i:8;s:8:"channels";i:3;s:4:"mime";s:10:"image/jpeg";}
  _oembed_f5bea5d5305fc5e79bbd149be3ddbaa0: "{{unknown}}"
  _oembed_3898069246f9bef36e139263b85efdd6: "{{unknown}}"
  _oembed_1e0043e44616e8131026f855a9e7ae1c: "{{unknown}}"
  _oembed_77f67615e35cfaf7ef5bb8243c08c218: "{{unknown}}"
  _oembed_1a20563d3d0c181df8836b5107e97deb: "{{unknown}}"
author:
  login: andrewjw
  email: andrewjwilkinson@gmail.com
  display_name: Andrew Wilkinson
  first_name: Andrew
  last_name: Wilkinson
permalink: "/2010/06/30/continuous-integration-testing/"
---
<a href="http://www.flickr.com/photos/mythoto/2917647893/"><img src="{{ site.baseurl }}/assets/2917647893_e04eba796c_m.jpg" alt="rom whence the brick came by mythoto" style="float:right;border:0;" /></a>At work we recently set up <a href="http://buildbot.net/">Buildbot</a> to replace an in-house continuous integration tool that never really took off.  I've used Buildbot before, in a hobby capacity, but using it my day job has really brought home to me how important not only testing is, but testing continuously.n
Buildbot is pretty simple to explain. Every time you make a commit to your source control system this triggers buildbot to run a series of steps over your code. What these steps are is totally configurable by you. Typically though, you'll configure it to check out your code, compile it and run unit tests.n
I'm a big fan of test driven and issue driven development. With these two methodologies when you want to make a change you record the issue in your bug tracking software, then write a test that detects the deficiency in your code. Once you've done that you can start actually making the change that you wanted to make in the first place.  By writing down the issue you're forced into thinking about the change that you want to make, and creating the test ensures that you know when it's complete.n
TDD and IDD are useful things to aim for, but in reality you'll probably fall short sometimes. Not everything can be unit tested easily, or you might be under significant time pressures that force you to cut corners. One of the projects I manage has a test suite that takes 25 minutes to run. If I'm getting phone calls urging me to fix a problem as soon as possible then I can't wait for the tests to run before I commit the change.n
Because builtbot runs without user intervention you don't need to remember to do anything. Buildbot is also a nag. If you introduce a bug with a change you quickly get an email letting you know that there is a problem, and if you set those emails up to go to your team then you also have peer pressure to get that problem fixed.n
I spend most of my time building <a href="http://www.djangoproject.com">Django</a> based sites. For these sites I set up six steps for Buildbot to follow. The first step is the checkout step, then a step to copy a settings file into place. Django stores settings in a Python file and these settings need to be configured for each server that the site is run on. I typically have a file <tt>settings_local.py.buildbot</tt> stored in the repository and this step copies this file to <tt>settings_local.py</tt> so the following commands will run with the correct settings. The next step is to download and install the dependencies of the site. I'm going to go into more detail on how I manage settings and dependencies in a future post, but Buildbot just runs the correct commands.n
The first three steps that Buildbot runs are just configuration steps. The first of the real test is a simple compilation step. It's rare that a change gets committed without it ever being run, but it's still worthwhile to check that the code compiles. It is possible that when merging changes from different branches errors can creep in. Fortunately Python makes it easy to check that all the files in a directory structure compile using the <tt>compileall</tt> module. This can be run using the command <tt>python -m compileall -q</tt> which return an exit code of zero if all the files compile, and nonzero if there is an error. This means that if there is an error Buildbot will detect it, and mark the build as failed.n
The next step I run is the unit tests. This where the bulk of the testing occurs. I'm not going to go into details on how to write unit tests, but assuming you have them this assures you that your tests pass after every commit. Because Buildbot can be easily configured to build on several different machines on each commit you can easily test that a change you made on a Python 2.5 machine also works on a Python 2.4 machine.n
The final step I run is <a href="http://www.logilab.org/857">PyLint</a>. PyLint checks that your code complies with a set of coding standards and simple checks. If your unit tests don't have a 100% coverage (and frankly, whose does?) then PyLint will hep detect that there are no obvious flaws in your code. PyLint takes a bit of time to configure, especially as it doesn't like some of the metaclass magic that Django uses, but once you have a configuration file written PyLint is an excellent final check.n
Hopefully this has given you a flavour of what Buildbot can do for you, and if you're in a team or are building a cross-platform piece of software then Buildbot really needs to be there, watching your back.n
Photo of <a href="http://www.flickr.com/photos/mythoto/2917647893/">from whence the brick came</a> by <a href="http://www.flickr.com/photos/mythoto">mythoto</a>.n