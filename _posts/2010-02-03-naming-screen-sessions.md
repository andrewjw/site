---
layout: post
title: Naming Screen Sessions
date: 2010-02-03 13:27:53.000000000 +00:00
tags:
- command line
- django
- linux
- screen
- unix
permalink: "/2010/02/03/naming-screen-sessions/"
---
I develop a number of Django-powered websites at work, and usually I want to leave them running when I'm not working on them so others can check out my progress and give me suggestions. The Django development server is incredibly useful when developing, but it's not detached from the terminal so as soon as you log out the server gets switched off. One alternative is to run the website under Apache, as you would deploy it normally. This solves the problem of leaving the website running, but makes it much harder to develop with.

A third option is the GNU program <a href="http://www.gnu.org/software/screen/">Screen</a>. When run without arguments <tt>screen</tt> puts you into a new <tt>bash</tt> session. Pressing <tt>Ctrl+d</tt> drops you back out to where you were. The magic occurs when you press <tt>Ctrl+a d</tt>. This drops you back out, but the <tt>bash</tt> session <b>is stilling running!</b> By typing <tt>screen -r</tt> you'll reattach to the session and can carry on working as before. You can leave it as long as you like between detaching and reattaching to a session, as long as the computer is still running.

It is possible to run multiple screen sessions at once, perhaps with a different Django development server running in each. Unfortunately <tt>screen</tt> will only reattach automatically when there is just one detached session. If you have more than one then you'll be confronted by a cryptic series of numbers that uniquely identifies each session. You can reattach to a specific session you can type <tt>screen -r &lt;pid&gt;</tt>.n
To make things easier to reattach to the session that I'm working on I give these sessions name so rather than a cryptic series of numbers I see a useful set of names. To do this you just need to type <tt>Ctrl + A : sessioname &lt;name&gt;</tt>.

There are plenty of other useful things that <tt>screen</tt> can do, but named sessions is by far and away the most common one that I use.
