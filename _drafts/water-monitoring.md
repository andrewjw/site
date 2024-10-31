---
layout: post
title: Water Monitoring
date: 2024-11-07
tags: prometheus grafana
permalink: "/2024/11/07/water-monitoring/"
---
In some of my previous posts I talked about my journey towards (monitoring every aspect of my home)[/2020/10/14/house-measurements/].
For a long time now I've been measuring temperatures, (electricity and gas usage)[/2020/12/02/meter-readings-over-mqtt/], solar power
and more. One area that has long been on my target list was our water usage - not least because a few years ago we had a leak that
went undetected until became a fairly significant problem. Recently while my plumber was doing our annual gas boiler service I asked
him to fit a water meter which has allowed me to finally start tracking this data.

The key discovery that allowed me to do this was that you can get "pulsed" water meters (I used (this model)[https://www.bmeters.com/en/products/gsd8-i/]
from B-Meters. They come preequipped with an inductive reader, and have a couple of wires you can connect to that receive a pulse for
every litre of water used. Installing the meter was relatively straightforward for my plumber, despite the cramped space he had available.


