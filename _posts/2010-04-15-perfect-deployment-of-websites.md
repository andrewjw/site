---
layout: post
title: Perfect Deployment Of Websites
date: 2010-04-15 13:17:32.000000000 +01:00
tags:
- deployment
- django
- fabric
- pip
- virtualenv
- web development
permalink: "/2010/04/15/perfect-deployment-of-websites/"
---
Recently I have been giving a lot of thought to how best to deploy websites, specifically Django powered
sites. In future posts I'll describe how I use some of tools available to deploy websites, but in this post I
want to set out the goals of any system that you use to deploy a website.

What do mean when we say deployment? Clearly it involves getting your code onto a production server but the
process also needs to look after any dependencies of your code. Updates also sometimes require database
changes and these need to be managed and deployed with the appropriate code changes. If your website is more
than just a hobby then it will also usually involve some sort of high availably set up.

The first requirement is repeatability. You might be able to follow a list of ten commands without making a
mistake normally, when your site is broken and you need to get a fix deployment as soon as possible following
that list will suddenly become a whole lot harder. For this reason, and to avoid the temptation to cut corners
when deploying a change automation of as much as possible is key.

The second requirement is scalability. As your website grows you deployment process needs to be able grow with
it. As you add a new server to your cluster you don't want to have to spend a long time updating your
deployment process, nor do you want the extra server to create extra work for you to do on every deployment.

Another requirement is speed. I'm usually very skeptical of anything that claims 'written for speed' as a key
benefit. Unless you know something is slow, it's usually better to make something easier to maintain than
quick. An automatic process will inevitably be quicker than a manual one and whether or not your deployment
process results in down time for your site the upgrade process is inevitably a risk and ideally that risk
window will be kept to a minimum.

Database migrations are a tricky thing to get right. A deployment system must allow developers to track
changes that they make to the database, and to make it easy to ensure these changes are applied at the right
moment.

In future posts I will talk about how tools such as fabric, virtualenv, pip and south can be used to
meet these requirements and ensure you never have a failed deployment again.
