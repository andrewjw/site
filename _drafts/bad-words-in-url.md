---
title: Bad Words In A URL
layout: post
---
Today I wanted to post about one of the more interesting debugging experience I've been involved in. This
happened quite a few years ago, when I was involved in migrating a set of websites over to use a single
login. The idea was that as soon as you landed on a site and your session wasn't logged in, you would be
bounced over to an authentication site, which would bounce you back again. The two sites would communicate
via a back channel, and if you were logged in on the authentication site the main site would log you to.
If not then you'll browse as a logged out user, and when you logged in you were be bounced over to the
authentication site with your credentials passed via a back channel. If successful then you were logged in
on both sites, otherwise an error was displayed.

The back channel communication was all encrypted with preshared keys, and when the user was bounced to the
authentication site they were also given an encrypted token to ensure that a bad actor couldn't attempt to
hijack another user's session. The exact details of the token aren't important, but they included the user's
session id, details of the site they landed on, and the time they were bounced (to prevent against replay
attacks).

Everything was working great in testing, and we gradually rolled the change out to more and more users.
Eventually though we started getting reports of a small number of users not being able to log in. We
were able to determine that the landed on the main site ok, and were bounced to the authentication site,
but never arrived there.

A considerable amount of back and forwards with the clients ensued, trying to determine what caused the
issue. What made it even stranger is that it was only intermittent. It would start or stop working seemingly
at random. For some companies it worked fine for everyone, but for others everyone would have an occasional
problem.

I don't remember how we actually discovered the cause, but it was due to the company's proxy blocking
urls that contained a "bad word". Obviously we weren't intentionally sending naughty words, but what we
were doing is base 64 encoded essentially random data. Because base 64 encoded uses all the normal
alpha-numeric characters, if you generate enough strings eventually you'll get some English words included
in the output.

The solution was to add a random number to the beginning of our encoded data, and then test the output against
a list of bad words. If it matched we tried a different number, until we got a "clean" output. Once this
was deployed users behind the proxy no longer had trouble logging in.

So, the lesson is that if you're including data in your urls, particularly encoded random data - think about
whether you could possible get blocked. With enough users, someone will definitely hit that edge case.
