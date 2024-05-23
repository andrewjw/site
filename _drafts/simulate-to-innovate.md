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

At the beginning of the project, the project team needs to provide a business case to justify the investment into the project.
At this stage it needs to justify the work to build a simulation of the system, which will validate the physical design. Only once
that has been created will the company's board sign off on the money to proceed with the build. The company plan to sell an
additional ten thousand cookies per day, so the project team need a ball-park figure of how many ovens and packing stations
they need, so they can estimate the return on investment, and decide it is likely to fit into the physical space they have
available.

The first step is to gather some basic metrics about the different components in the system, in this case the ovens, packing stations
and conveyors to link them together. Following some research, the team came up with the required numbers - a conveyor can move 500 cookies
per hour, an oven can bake 1,000 cookies an hour using two conveyor lines, and a packer at one station can pack 300 cookies per hour.
Immediately the team spotted a problem - the factory currently works an 8-hour shift, so one oven can only bake 8,000 cookies per day -
below the company's 10k target. 

We haven't even made it to the stage of what could be called a "simulation", and already the work to get there is showing benefits.
Taking these numbers back to the business, along with the fact that the ovens are expected to have a 95% uptime, they agree to plan
for a two oven system, as that gives scope for growth, and the ability to keep baking during downtime for one oven.

The team now need to use this guidance and the numbers found in their research to calculate some ball-park figures to build a business case.
Even a calculation like _items picked per hour * number of stations * shift length * uptime_ will give you some useful numbers,
so that is what they do. For packing stations the equation becomes _300 * n * 8 * 0.99_. With `n=4` they could pack ~9500 cookies
per day, while `n=5` packs nearly 12k, giving a nice buffer above the company's target. They have already agreed to use two ovens,
the remaining question is how many conveyor lines. Using the same equation form they find _500 * n * 8 * 0.95_ tells them they need
three conveyor lines to hit the 10k target.

In the example of 
