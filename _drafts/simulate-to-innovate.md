---
layout: post
title: Simulate To Innovate
date: 2024-05-09
tags: management
---

The concept of a minimum viable product (popularised by Eric Reis in The Lean Start-Up *CONFIRM*) is pretty much
ubiquitous in modern software development. But what does minimum look like for software that interacts with the
physical world? If your software manages a physical process, such as a production line or a warehouse
process, then it's very likely that minimum means all features are implemented, and the physical process operates
with a desired efficiency level.

How can you test your software while the physical aspects are being built? And how do you know that the physical
design is optimal? The answer is to simulate as much as possible, as early as possible.

A simulation can be anything from a simple spreadsheet formula, to a 3d visualisation with realistic
moving parts to show the expected physical behaviours. How much effort you should put into the simulation depends
on what stage of the project you're at, and how impactful being wrong would be. At a project conceptualisation stage,
you can likely afford to have a rough calculation that gives you numbers in the right ballpark. The closer you
get to confirming the physical design, beyond which point changes become exponentially more expensive, the more
detail you need. Lastly, as your physical build progresses, and your software development continues, your simulation
should have increasingly more fidelity to give your software developers an accurate testing environment to give you
confidence that the software and hardware will work together as intended, from the moment you go live.

Let's take as an example a business that wants to build a new cookie baking line. The raw materials are mixed, baked in
an oven, packed and then shipped. As well as physically installing the conveyors, ovens and packing stations they need
to create the software that manages the flow of products, to ensure they spend the right amount of time in the oven, and
that the products are packed onto the right pallets, to be sent to the correct customer.

At the beginning of the project the project team need to provide a business case to justify the investment into the project.
At this stage it needs to justify the work the build a simulation of the system, to validate the physical install. Only once
that has been created will the company's board sign off on the money to proceed with the build. The company plan to sell an
additional ten thousand cookies per day, so the project team need a ball-park figure of how many ovens and packing stations
they need, so they can estimate the return on investment, and decide it is likely to fit into the physical space they have
available.

Even a calculation like _items picked per hour * number of stations * shift length * uptime_ will give you some ball-park
figures to use in discussions about the project.

In the example of 
