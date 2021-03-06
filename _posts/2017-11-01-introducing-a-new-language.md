---
layout: post
title: Introducing A New Language
date: 2017-11-01 21:56:35.000000000 +00:00
tags:
- management
- decision making
- java
- kotlin
- programming
- scala
permalink: "/2017/11/01/introducing-a-new-language/"
flickr_user: 'https://www.flickr.com/photos/ruiwen/'
flickr_username: Ruiwen Chua
flickr_image: 'https://live.staticflickr.com/3324/3260095534_d1f216fb8a_w.jpg'
flickr_imagelink: 'https://www.flickr.com/photos/ruiwen/3260095534/'
flickr_imagename: 'code.close()'
---
[At work](https://ocadotechnology.com/), there is a discussion going on at the moment about
introducing [Kotlin](https://kotlinlang.org/) into our tech stack. We're a JVM based team, with the
majority of our code written in Java and few apps in [Scala](https://www.scala-lang.org/). I don't
intend to discuss the pros and cons of any particular language in this post, as I don't have enough experience
of them to decide yet (more on that to come as the discussion evolves). Instead, I wanted to talk about
_how_ you can decide when to introduce a new language.

Programmers, myself included, have a habit of being attracted to anything new and shiny. That might be a new
library, a new framework or a new language. Whatever it is, the hype will suggest that you can do more, with
less code and fewer bugs. The reality often turns out to be a little different, and by the time you have
implemented a substantial production system then you've probably pushed up against the limits, and found areas
where it's hard to do what you want, or where there are bugs or reliability problems. It's only natural to
look for better tools that can make your life easier.

If you maintain a large, long-lived code base then introducing anything new is something that has to be
considered carefully. This is particularly true of a new language. While a new library or framework can have
its own learning curve, a new language means the team has to relearn how to do the fundamentals from scratch.
A new language brings with it a new set of idioms, styles and best practices. That kind of knowledge is built
up by a team over many years, and is very expensive both in time and mistakes to relearn.n Clearly, if you
need to start writing code in a radically different environment then you'll need to pick a new language. If
like us, you mostly write Java server applications and you want to start writing modern web-based frontends to
your applications then you need to choose to add Javascript, or one of the many Javascript based languages,
into your tech stack.
<!--more-->

The discussion that we're having about Java, Scala and Kotlin is nowhere near as clear-cut however.
Fundamentally choosing one over the other wouldn't let us write a new type of app that we couldn't write
before, because they all run in the same environment. Scala is functional, which is a substantial change in
idiom, while Kotlin is a more traditional object-orientated language, but considerably more concise than Java.

To help decide it makes sense to write a new application in the potential new language, or perhaps rewrite an
existing application. Only with some personal experience can you hope to make a decision that's not just based
on hype, or other people's experiences. The key is treat this code as a throw-away exercise. If you commit to
putting the new app into production, then you're not investigating the language, you're commiting to add it to
your tech stack before you've investigated it.

As well as the technical merits, you should also look into the training requirements for the team. Hopefully
there are good online tutorials, or training courses available for your potential technology, but these will
need to be collated and shared, and everyone given time to complete them. If you're switching languages then
you can't afford to leave anyone behind, so training for the entire team is essential.

Whatever you feel is the best language to choose, you need to be bold and decisive in your decision making. If
you decide to use a new language for an existing environment then you need to commit to not only writing all
new code in it, but to also fairly quickly port all your existing code over as well. Having multiple solutions
to the same problem (be it the language you write your server-side, or browser-side apps in, or a library or
framework) create massive amounts of duplicated code, duplicated effort and expensive context switching for
developers.

Time and again I've seen introducing the new shiny solution create a mountain of technical debt because old
code is not ported to the new solution, but instead gets left behind in the vague hope that one day it will
get updated. New technology and ways of working can have a huge benefit, but never underestimate the cost, and
importance, of going all the way.
