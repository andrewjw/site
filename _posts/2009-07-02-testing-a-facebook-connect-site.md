---
layout: post
title: Testing A Facebook Connect Site
date: 2009-07-02T11:17:59.000Z
tags:
  - web development
  - development
  - facebook
  - social
permalink: /2009/07/02/testing-a-facebook-connect-site/
---
I've been developing a [website](http://www.tvutopia.net) in my spare time. Because I want to add plenty of
social features it makes sense to let users login using Facebook Connect. The Facebook platform is by far the
most successful social platform with many developers having created applications and websites that use it. I
expected that the experience for developers would be a good one. Unfortunately, I was disappointed.

Facebook makes it easy to register an application and provide links to libraries that wrap their API and make
it easy to get started. What Facebook don't provide however is a downloadable version of their API to test
with. Facebook have made some effort to support [test
users](http://wiki.developers.facebook.com/index.php/Test_Accounts), but you have to open ports in your
firewall and use your real facebook account to test with. Testing a new user signing up for your app is really
quite a chore. Automating this sort of test is essentially impossible.

In an ideal world Facebook would produce a downloadable program that you can use to automatically user,
programmatically log in users and generally automatically test all the parts of your code. The danger is that
they'd have to give you a downloadable copy of their website code. Google App Engine give a similar
downloadable environment, and you can't say that Google don't have a load of code that they don't want to give
away!

The Facebook API is pretty simple to get started with, and with in a couple of minutes you'll have the code
written to log a user in. Checking that it all works though, is a much tougher challenge...
<!--more-->
