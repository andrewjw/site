---
layout: post
title: Swapping To Fire Fighting Mode
date: 2024-10-01
tags: leadership
permalink: "/2024/10/01/swapping-to-fire-fighting-mode/"
---
In an ideal world, developers would write code, create their tests, and get ready for deployment.
There might be a user acceptance testing step, and then your code would be released, bug-free, to
users. The real world is rarely this simple, and despite your best laid plans, your
deployment could introduce many bugs that need to be dealt with.

In the event of a problematic deployment your first thought should be rollback to a known good
version. This a good step, but does require thought during development to allow it. A deployment
to enable to a new code path is straightforward to roll back, particularly if you protect it with
a feature flag. Any change that that modifies a data store, relies on changes to external systems or
even requires real world processes to be changed are much harder to revert, and you might be forced
to fix forward.

A single code change to fix a bug isn't too much work, but what if you're faced with multiple
issues that are being reported over a number of days. In this situation you need to help your
team switch from normal day-to-day mode into firefighting work, and as a leader you need to create
space for your team(s) to pivot and get the situation under control.

To do this follow three steps, highlight, coordinate and push back.

The first step is to ensure that everyone in the team is aware of the gravity of the situation. It's
common for people to not immediately pick up on incidents. Generally, as a leader that's what you want
- allow the on-call person to deal with any situations, and for other members to get on with their planned
work as normal. In this situation though you want everyone to look at what issues are being raised and to
prioritise them over their existing work.

A complex, long-term incident will almost certainly involve more than one team. Your incident management
processes will hopefully already been adept at dealing with single incidents that cross team boundaries,
but what about multiple complex issues, which might not meet the threshold to be declared an "incident"?
This is where you have to step in as a leader and work to ensure that nothing is falling between the cracks.
