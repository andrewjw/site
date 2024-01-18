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
an application is more than just a server with a CPU, some memory and disk. Instead it is a whole ecosystem of 
