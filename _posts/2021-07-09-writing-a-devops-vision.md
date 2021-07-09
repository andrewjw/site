---
layout: post
title: Writing A DevOps Vision
date: 2021-07-09
tags:
- management
- devops
permalink: "/2021/07/09/writing-a-devops-vision/"
flickr_user: 'https://www.flickr.com/photos/141857125@N02/'
flickr_username: Ditmar Kuhnt
flickr_image: 'https://live.staticflickr.com/1820/30163620418_ff376f2b6a.jpg'
flickr_imagelink: 'https://www.flickr.com/photos/141857125@N02/30163620418'
flickr_imagename: 'pipelines'
---
DevOps as a concept has been around since around 2010, but implementing the ideas behind it,
particularly when you're in a team that is supporting old monolithic codebases is challenging.
For several years we had engineers fulfilling the role of a "DevOps Engineer". However, we
always knew that having a specific person working on DevOps is a bit antithetical to the
DevOps concept - it's supposed to be a state of mind and a set of practices rather than a job role.

The aim was always to have that engineer act as a source of expert knowledge and an enabler. Teams
were still supposed to own their code, processes and deployments, but in reality, DevOps related
work was often thrown over the wall to that engineer with the expectation that it was their
problem, and not the team's problem.

We ended up in a situation where we had to make a choice - hire a new engineer into the same role,
or attempt to spread the work across all engineers. We chose the second option, but that then poses
the question of how to change team culture across a department, so that DevOps becomes a standard part
of the team's process, much like Kanban, Scrum or any of the other ways the team organises themselves.
<!--more-->

When introducing this change I wanted to ensure three things, that people understood what the
scope of the change was, why it was important, and that there was help available to aid them in taking
on this responsibility.

Changes such as this need some careful thought before they are rolled out - as well as needing to
persuade people that they are a good idea, and to reassure them that they will be supported
through the change, you need to make sure the changes actually happen. When asking a team to change
their processes there is a significant amount of inertia to overcome, and a real danger that they
just shrug their shoulders and say "that's just management waffling on about nothing important".

To make sure the new process achieves its goals I followed a three-step process. Firstly I prepared
a document describing the change, which covered all the points above and can be referred back to in the
future. Secondly, I presented the process during a town hall. This ensured that people couldn't claim
to have not read the document! Finally, I kicked off a project to improve our build pipeline reliability.

The key part of the document is the section that describes the changes I wanted to enact. To make
this as clear as possible I structured it as a series of bullet points preceded by "Teams should..."
Each bullet point is a short behaviour, followed by a longer piece of explanatory text. To try to
ensure the document made an impact these were phrased deliberately stridently, perhaps even controversially,
to try and provoke some interaction.

It's probably too early to declare the change a success or not, but there are encouraging signs.
Teams are working well together to align on processes, they are taking responsibility for their builds,
and the quality of our pipelines is improving.

So if you want to make a cultural change, then I suggest following these three steps - document the change,
present the change, and then start a project to initially force the change you are looking for, with the
aim that it will continue long beyond the project itself.
