---
layout: post
title: Strict Development
date: 2009-05-07 12:28:34.000000000 +01:00
type: post
parent_id: '0'
published: true
password: ''
status: publish
categories:
- etiquette of programming
tags:
- best practice
- development
- issue driven development
- test driven development
meta:
  _edit_last: '364050'
author:
  login: andrewjw
  email: andrewjwilkinson@gmail.com
  display_name: Andrew Wilkinson
  first_name: Andrew
  last_name: Wilkinson
permalink: "/2009/05/07/strict-development/"
---
While working on my new open source project, <a href="http://code.google.com/p/couchql/">CouchQL</a>, I'm being very strict with my development process and following both issue driven development, and test driven development.n
Issue driven development requires that every commit refers to an issue that has been logged in the bug tracking software. This means that every change must be described, accepted and then logged. This works better if your repository is connected to your bug tracking software such that any commit message with a issue number is automatically logged. In subversion this can be achieved with a post commit hook, such as <a href="http://trac.edgewall.org/browser/trunk/contrib/trac-post-commit-hook">this script</a> for trac.n
The connection between your commit messages and bug tracking software means that when changes are merged between branches new messages will be added to the issue, informing everyone what version of the software the issue has been fixed in. As well as just adding comments to issues it is also possible to mark bugs as fixed with commit messages such as "Fixes issue #43." which should speed up your work flow. While Google Code does add hyperlinks between commit messages and issues, it doesn't add automatically add comments, which is a pain.n
Enforcing a development practice like this requires you to think about the changes you are making to your software, and focuses your mind one a particular goal. Bug tracking software will have the ability to assign priorities to changes as well to group them into milestones. This helps you to build up a feature list for each version of the software, and to know when you've achieved your goals and it's time to release!n
Test driven development is related in that before any changes to code are made a test must be written. This test must be designed to check the result of the change as closely and completely as possible. When the test passes (and all other tests still pass) the change that you were making is complete.n
The benefits to this style of development are two fold. Firstly it should be easy to end up with test coverage of close to 100%. Secondly it forces you to think about the point of the change that you're making. Combine this with the issue that you logged before you started, and you'll really have a good idea of the scope and aim of your change before you ever touch the keyboard.n
It can sometimes be hard to do this on every change you make, but the more often you do the better tested and more maintainable your code will be. Tools can really help you. If your version control system is linked to you bug tracking software then all you need to do is remember to log a bug and mention it in every commit message.  A continuous integration testing tool such as buildbot makes keeping your tests complete very desirable as you'll be notified of any breakages very quickly.n
You can't be made to follow development processes such as these, but if you understand the benefits, and want to use then they become second nature, and hopefully you'll be a better programmer as a result.n
