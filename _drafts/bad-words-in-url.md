---
title: Bad Words In A URL
layout: post
date: 2020-10-28
tags:
- debugging
- base64
permalink: "/2020/10/21/bad-words-in-a-url/"
flickr_user: 'https://www.flickr.com/photos/tadsonbussey/'
flickr_username: Tadson Bussey
flickr_image: 'https://live.staticflickr.com/64/160251864_5093ae131f_w.jpg'
flickr_imagelink: 'https://www.flickr.com/photos/tadsonbussey/160251864/'
flickr_imagename: 'Dead End, DeKalb, IL'
---
Today I wanted to share one of the more interesting debugging experiences that I've had. This
happened quite a few years ago when I was involved in migrating a set of websites over to use a single
login. The idea was that as soon as you landed on a site and your session wasn't logged in, you would be
bounced over to an authentication site, which would bounce you back again. The two sites communicated
via a backchannel, and if you were logged in on the authentication site the main site would log you in too.
If not then you'd browse as a logged-out user, and when you logged in you were bounced over to the
authentication site with your credentials passed via a backchannel. If successful then you were logged in
on both sites, otherwise an error was displayed.

The backchannel communication was all encrypted with preshared keys, and when the user was bounced to the
authentication site they were also given an encrypted token to ensure that a bad actor couldn't attempt to
hijack another user's session. The exact details of the token aren't important, but they included the user's
session-id, details of the site they landed on, and the time they were bounced (to prevent against replay
attacks).

Everything was working great in testing, and we gradually rolled the change out to more and more users.
Eventually, we started getting reports of a small number of users not being able to log in. We
were able to determine that they landed on the main site ok, and were bounced to the authentication site,
but never arrived there.
<!--more-->

A considerable amount of back and forwards with the clients ensued, trying to determine what caused the
issue. What made it even stranger is that it was only intermittent. It would start or stop working seemingly
at random. For some companies, it worked fine for everyone, but for others, everyone would have an occasional
problem.

I don't remember how we discovered the cause, but it was due to the company's proxy blocking
URLs that contained a "bad word". We weren't intentionally sending naughty words, but what we
were doing is base 64 encoded essentially random data. Because base 64 encoded uses all the normal
alpha-numeric characters, if you generate enough strings eventually you'll get some English words included
in the output (see the [infinite monkey theorem](https://en.wikipedia.org/wiki/Infinite_monkey_theorem)).

The solution was to add a random number to the beginning of our encoded data and then test the output against
a list of bad words. If it matched we tried a different number, until we got a "clean" output. Once this
was deployed users behind the proxy no longer had trouble logging in.

So, the lesson is that if you're including data in your URLs, particularly encoded random data - think about
whether you could possible get blocked. With enough users, someone will be using a strict proxy and will hit that edge case.
