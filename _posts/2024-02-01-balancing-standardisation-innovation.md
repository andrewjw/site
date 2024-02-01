---
layout: post
title: Balancing Standardisation With Innovation
date: 2024-02-01
tags: management
permalink: "/2024/02/01/balancing-standardisation-innovation/"
image: robot_coding_standards.jpeg
image_title: A robot changing a list of coding standards.
image_credit: Image created with Bing Image Creator.
---

In my earlier post [Sustainable Software Development](https://www.theandrewwilkinson.com/2023/12/07/sustainable-software/)
I talked about how to build software that can be maintained and improved over the long term, and how to run teams that can
work without burning out. In this post, I want to expand on one area of this - how to maintain innovation while using standards
to reduce diversity in your code base.

Snow-flake applications, which have unique characteristics compared to others in your estate, take a significantly outsized amount
of time to maintain. This extra complexity requires specialist knowledge in your developers, and the time taken to context switching
between applications is increased. You also don't benefit from the economies of scale, where you can apply improvements across many
of your applications simultaneously.

Historically, sharing code across applications would be done through shared libraries, but the modern software development landscape
is more complex and many companies are moving to Platform-as-a-Service models (PaaS). This is where the infrastructure used to run
an application is more than just a server with a CPU, some memory and a disk. Instead, it is a whole ecosystem of APIs, developer tools
and a platform for running code. Whether internally developed, or purchased from an external company, PaaS systems are chosen because
they abstract developers away from much of the drudgery that previously they would have had to work through, but this also constrains
them to only using services provided by the platform.

<!--more-->

PaaS is not the only form of standardisation though, companies will usually have policies (whether implicit or explicit) that they only
use certain languages, frameworks, third-party libraries or design patterns to build their applications. However standardisation
is enforced, the end result is the same - developers trade off increased speed of delivery and reduced cognitive load against reduced
freedom to write code as they wish.

What happens if you want to do something that doesn't fit with your PaaS platform? Or perhaps your company has standardised on Java
but you would like to write some code in Kotlin, or maybe Python? Maybe a new build tool has been released that you think will offer
quicker builds or simpler configuration, speeding up your cycle time. Whatever the reason, changing the status quo is hard, but
feeling like you are forced to stick with what is currently used is devastating for a developer's morale.

As a leader, you need to balance the benefits of standards against the threat of stagnation. While standards give you benefits with
current development, you also need a defined policy to change the standard, and a process to update existing code to match the new rules.
If you don't then your teams may be missing out on improved ways of working as the technological landscape evolves.

To allow for innovation you need to create time for developers to experiment, with the expectation that the code written will often not
be deployed into production. Whether or not an experiment is successful is not important - what matters is that you learn one way or
the other. This innovation could take the form of 10% time, or just giving developers flexibility to add experiments onto the team roadmap
with low friction. While hackathons are a good way to build experimental new apps, they aren't good at changing standards. Firstly they
usually come around too infrequently, and with the goal of building something that you can demo they don't lend themselves well to more technical
or process experiments.

As well as providing time for developers to experiment, you also need to supply motivation. If developers see ideas for improvements
being shot down without proper consideration, if they don't understand why they were rejected, or worst of all if suggestions
languish with no decision either way then people will not choose to put themselves forward to experiment. Instead, they will feel like they
have to suffer with the current processes, even though they believe that it can be improved. This is terminal for morale, and productivity.

Once you have created a standard, and provided space to propose changes to it, the next step is to document the process for proposing those
changes, how they will be judged (and by whom), and how they will applied. How this will work depends on the size and structure of your
organisation. You might have an individual architect or head of engineering who would make sense as a decision-maker, even better would
be a group of developers who can act as an architectural council. There should be a list of criteria that will be applied, so people know
what to address in their proposal. Some examples could include the effect on running costs, the learning curve for other developers, or the effect on the
speed of feature implementation (perhaps by reducing the number of lines of code that need to be written).

Applying a change in standards to your existing code base can be painful. It's important to approach it actively though, otherwise code that
follows the old standard just becomes technical debt. You need to identify areas where the legacy method is used, and create a project or
projects to update them. This won't happen overnight, but scheduling this alongside a team's other work is needed to avoid the old code
languishing until it is forgotten about.

How do you handle standardisation in your teams? Have you found a way to encourage innovation while maintaining a coherent code base?
Please let me know in the comments below!
