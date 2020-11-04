---
title: Glow Bright
layout: post
date: 2020-11-04
tags:
- electricity
- gas
- glow
permalink: "/2020/11/04/glow-bright/"
---
When my electricity provider, nPower, upgraded me to a smart meter I was excited about getting access to more
data about my electricity and gas usage. Unfortunately, it turned out that the extra data provided by the
connected meters was only available to the power supplier, and not to me as a consumer. They provided a little
device with a screen (known as an IHD, or in-home device) which displayed the current and daily/weekly/monthly
usage, but little else. No mobile app, no ability to dig into your historical usage, and definitely no API access.

While I was disappointed and frustrated about not having access to what I consider be my data, I left it as I
had more important things to worry about (i.e. kids). With my recent project to look at collecting more data from
my house, I wanted to revisit this, and collect the data.

There are two meter standards in the UK, SMETS1 and SMETS2. SMETS1 is the older standard, which is no longer being
rolled out. SMETS2 is the current standard, which operates quite differently to SMETS1. The main benefit being that
if you switch provider your smart meter will continue to work, something that wasn't true with the earlier standard.
If you're unlucky enough to have a SMETS1 meter you can ask for it to be upgraded. Fortunately, I had a SMETS2 meter.

The way these meters work is that both the electricity and gas meters broadcast their readings locally over a ZigBee
network. This is picked up by your IHD, and displayed live. The electricity meter also listens to the gas readings
and every so often uploads them over a mobile phone connection to a central data broker. This is then forwarded on
your supplier. [smartme.co.uk](https://www.smartme.co.uk/technical.html) has much more detail on this process.

The key point is that your data can not only be forwarded on to your supplier, but you can grant access to other
companies too. Enter [Glow](https://shop.glowmarkt.com/) who act as what is known as `DCC Other User` and use
smart meter data to help companies do research and development. They also provide more tools for consumers to use
their data.

After installing the app you need to go through a security verification process. This involves uploading
details of your electricity meter and address (by taking photos of your bill), a photo of some photo id, and a
selfie video of yourself saying "I'm My Name, and I accept the terms and conditions". After that, your details
are sent away for a manual verification process, which in my case took two days. I also received an email
asking whether I was planning to buy their
[display](https://shop.glowmarkt.com/products/display-and-cad-combined-for-smart-meter-customers). When I said yes
they said they wouldn't process my application until it arrived. This was a bit frustrating as it meant I couldn't
use the app in the meantime. Once the device arrived the application was processed quickly.
<!--more-->

![Unboxing The Glow IHD](/assets/glow_unboxing.jpg)

![The Glow IHD Welcome Screen](/assets/glow_welcome.jpg)

![The Glow IHD Wifi Password](/assets/glow_wifipassword.jpg)

![The Glow IHD Meters Display](/assets/glow_meters.jpg)

The device itself works ok but does have a few usability issues. For example, the graphs could be designed better.
As the example below shows, it doesn't always pick the best axis.

![The Glow IHD Picking A Bad Graph Axis](/assets/glow_sillygraph.jpg)

That's a relatively minor point though, and generally, it does what it's supposed to do. I've had one occasion so far
when it lost its WiFi connection, but a quick reboot sorted that out. The main benefit comes from the fact that you
can access your live meter data over MQTT, and I'll talk about that in my next post.
