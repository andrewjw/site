---
layout: post
title: Balancing Standardisation With Innovation
date: 2024-02-01
tags: management
permalink: "/2024/02/01/balancing-standardisation-innovation/"
---

Previously I posted about [Sustainable Software Development](https://www.theandrewwilkinson.com/2023/12/07/sustainable-software/)
where I talked about how to build software that can be maintained and improved over the long term, and running teams that can
work without burning out. In this post, I want to expand on one area of this - how to maintain innovation while using standards
to reduce diversity in your code base.

Snow-flake applications, which have unique characteristics compared to others in your estate, take a significantly outsized amount
of time to maintain. The extra complexity requires specialist knowledge in your developers, and time taken to context switching between
applications is increased. You also don't benefit from the economies of scale, where you can apply improvements across many of your
applications simultaneously.

Historically, sharing code across applications would be done through shared libraries, but the modern software development landscape
is more complex and many companies are moving to Platform-as-a-Service models (PaaS). This is where the infrastructure used to run
an application is more than just a server with a CPU, some memory and disk. Instead, it is a whole ecosystem of APIs, developer tools
and a platform for running code. Whether internally developed, or purchased from an external company, PaaS systems are chosen because
they abstract developers away from much of the drudgery they previously would have had to work through but constrain them to only using
services provided by the platform.

PaaS is not the only form of standardisation though, companies will usually have policies (whether implicit or explicit) that they only
use certain languages, frameworks, third-party libraries or design patterns to build their applications. However standardisation
is enforced, the end result is the same - developers trade off increased speed of delivery and reduced cognitive load against reduced
freedom to write code as they wish.

What happens if you want to do something that's doesn't fit with your PaaS platform? Or perhaps your company has standardised on Java
and would like to write some code in Kotlin, or maybe Python? Maybe a new build tool has been released that you think will offer
quicker builds or simpler configuration, speeding up your cycle time. Whatever the reason, changing the status quo is hard, but
feeling like you are forced to stick with what is currently used is devastating for a developer's morale. You might also be missing
out on improvements if you stick to your standards too strictly.

As a leader, you need to balance the benefits of standards against the threat of stagnation. While standards give you benefits with
current development, you also need a defined policy to change the standard, and a process to update existing code to match the new rules.

