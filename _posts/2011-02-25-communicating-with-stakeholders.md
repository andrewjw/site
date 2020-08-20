---
layout: post
title: Communicating With Stakeholders
date: 2011-02-25 14:04:09.000000000 +01:00
type: post
tags:
  - bugzilla
  - communication
  - forbugz
  - etiquette of programming
permalink: /2011/02/25/communicating-with-stakeholders/
flickr_user: 'https://www.flickr.com/photos/pshanks/'
flickr_username: "Paul Shanks"
flickr_image: 'https://live.staticflickr.com/170/411196422_343c0965a8_w.jpg'
flickr_imagelink: 'https://www.flickr.com/photos/pshanks/411196422/'
flickr_imagename: 'Communication'
---
Last week I had a discussion with my boss about the best way to communicate with my stakeholders about the
progress of any work that they have asked my team to do. The question basically became how much information
should be communicated during a project. The requirements and delivery phases obviously require close
communication, but what is appropriate while the developers are hard at working, churning out code? If, like
me, you are required to work a number of disparate departments then the people in the departments may want to
know what work is currently on your plate before they ask you to do something. What's the best way to keep a
status board up to date?

Traditionally we have had a [Bugzilla installation](http://www.bugzilla.org/) which was used to
store a record of almost every change we made. A 
[subversion post commit hook](http://mikewest.org/2006/06/subversion-post-commit-hooks-101) allows us
to link every commit back to a piece of work in Bugzilla. This works well for coding in an
issue-driven-development style, but does result in Bugzilla sending a lot of emails. Many of which are
completely irrelevant to people outside of IT. Indeed even people inside IT, but who aren't directly linked to
that piece of work, don't need to be informed by email of every checkin.

Recently we have begun to experiment with [FogBugz](http://www.fogcreek.com/fogbugz/). While
similar to Bugzilla it has a number of subtle differences. Firstly FogBugz is designed to be used in a
helpdesk environment so it provides the ability to communicate both within the team and with external
stakeholders from the same interface. This gives you the ability to communicate on two different levels, with
all the communication still being tracked. The second difference is that FogBugz is not known amongst the
people outside of IT. Not all stakeholder know about Bugzilla, but some do, and some can even search and reply
using the webinterface. With FogBugz we'll take this ability away as, at least initially, only a limited
number of IT people will have access to the cases.

FogBugz had other project management advantages to Bugzilla. It allows you to create subcases to break down a
piece of work into more easily implemented chucks. It also has advanced estimation capabilities to allow you
to project how long a milestone will take to complete.

The crux of discussion is this: which is better, a known tool that provides complete access to status to those
that want it, or a tool that enables those doing the work to plan better but prevents those outside from
seeing how the work is progressing for themselves?

In my view developers should use the tools that they feel help them work the best. Looking at a list of tasks
is probably not going to help someone who is not doing the work to understand whether the project is on track
or not. However, it is important that stakeholders are kept informed of progress regularly so switching to a
less open development model should not be used as an excuse to become more insular, quite the opposite in
fact. Switching to a less open development model should force you to be more explicit and include status
updates as part of your regular working schedule.
