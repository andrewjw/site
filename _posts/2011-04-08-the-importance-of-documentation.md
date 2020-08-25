---
layout: post
title: The Importance Of Documentation
date: 2011-04-08 14:04:09.000000000 +01:00
tags:
    - code
    - documentation
    - ffmpeg
    - programming
    - etiquette of programming
    - qt
permalink: "/2011/04/08/the-importance-of-documentation/"
flickr_user: 'https://www.flickr.com/photos/geminicollisionworks/'
flickr_username: "Ian W Hill"
flickr_image: 'https://live.staticflickr.com/7626/16963020997_3005b7a514_w.jpg'
flickr_imagelink: 'https://www.flickr.com/photos/geminicollisionworks/16963020997/'
flickr_imagename: 'Books in progress'
---
Recently I've been working a couple of open source projects and as part of them I've been using some
libraries. In order to use a library though, you need to understand how it is designed, what function calls
are available and what those functions do. The two libraries I've been using are
[Qt](http://qt.nokia.com/) and [libavformat](http://www.ffmpeg.org/), which is part of
FFmpeg and they show two ends of the documentation spectrum.

Now, it's important to note that Qt is a massive framework owned by Nokia, with hundreds of people working on
it full-time including a number of people dedicated to documentation. FFmpeg on the other hand is a purely
volunteer effort with only a small number of developers working on it. Given the complicated nature of video
encoding to have a very stable and feature-full library such as FFmpeg available as open source software is
almost a miracle. Comparing the levels of documentation between these two projects is very unfair, but it
serve as a useful example of where documentation can sometimes be lacking across all types of projects, both
open and closed source.n So, lets look at what documentation it is important to write by considering how you
might approach using a new library.

When you start using some code that you've not interacted with before the first thing that you need is to get
a grasp on the concepts underlying the library. Some libraries are functional, some object orientated. Some
use callbacks, others signals and slots. You also need to know the top level groupings of the elements in the
library so you can narrow your focus that parts of the library you actually want to use.

Qt's document starts in a typical fashion, [with a
tutorial](http://doc.qt.nokia.com/4.7/gettingstartedqt.html). This gives you a very short piece of code that gets you up and running quickly. It then proceeds
to describe, line by line, how the code works and so introduces you to the fundamental concepts used in the
library. FFmpeg takes a similar approach, and links to a
[tutorial](http://www.inb.uni-luebeck.de/~boehme/using_libavcodec.html). However, the tutorial begins
with a big message about it being out of date. How much do you trust the out of date tutorial?

Once you've a grasp of the fundamental design decisions that were taken while building the library, you'll
need to find out what functions you need to call or objects you need to create to accomplished your goal.
Right at the top of the menu the [QT documentation](http://doc.qt.nokia.com/4.7/) has links to
class index, function index and modules. These let you easily browse the contents of the library and delve
into deeper documentation. [Doxygen](http://www.stack.nl/~dimitri/doxygen/) is often used to
generate documentation for an API, and it seem to be the way
[FFmpeg is documented](http://ffmpeg.org/doxygen/trunk/index.html). Their frontpage contains...
nothing. It's empty.

Finally, you'll need to know what arguments to pass to a function and what to expect in return. This is
probably the most common form of documentation to write so you probably (hopefully?) already write it. Despite
my earlier criticisms, FFmpeg does get this right and most of the function describe what you're supposed to
pass into the function. With this sort of documentation it's important to strike a balance. You need to write
enough documentation such that people can call your function and have it work first time, but you don't want
to write too much so that it takes ages to get to grips with or replicates what you could find out by reading
the code.n Some people hold on to the belief that the code is the ultimate documentation. Certainly writing
self-documenting code is a worthy goal, but there are other levels of documentation that are needed before
someone could read and the code and understand it well enough for it to be self-documenting. So, next time
you're writing a library make sure you consider:

* How do people get started? How do people navigate through the code? and, how do people work out how to call
* my functions?
