---
title: Meter Readings Over MQTT
layout: post
date: 2020-11-25
tags:
- electricity
- gas
- glow
- mqtt
- prometheus
- grafana
permalink: "/2020/11/25/meter-readings-over-mqtt/"
---
In a [previous post](/2020/11/04/glow-bright/) I talked about swapping the in-home device (IHD)
supplied by my electricty and gas company for one produced by [Glow](https://shop.glowmarkt.com/).
This connects over wifi and gives access to the raw data coming from your smart meters over [MQTT](https://mqtt.org/).
In order to collect this data an integrate it into my
[house monitor](https://www.theandrewwilkinson.com/2020/10/14/house-measurements/) I needed to listen to the MQTT
topic and expost the data to Prometheus.

This was quite similar to my previous project to expose [statistics from my router](
https://www.theandrewwilkinson.com/2020/10/21/router-stats-to-prometheus/), but as this was processing
JSON data being exposed over MQTT it was a lot simpler than parsing raw text over SSH. As before I created
[GitHub repo](https://github.com/andrewjw/glowprom) with my usual Python linting, testing and build scripts set up.

Connecting to MQTT is straightforward, using the [Paho MQTT library](https://pypi.org/project/paho-mqtt/). When they've
set up your MQTT account Glow's support team will supply you with a topic name that you can use, along with the username
and password you set, to connect. The code below shows how to do this. We'll cover the `on_message` callback next.
<!--more-->

```python
def connect(args, on_message):
    client = mqtt.Client()
    client.on_connect = functools.partial(on_connect, args.topic)
    client.on_message = on_message

    client.username_pw_set(args.user, password=args.passwd)
    client.connect("glowmqtt.energyhive.com", 1883, 60)

    client.loop_forever()
```

As you can probably guess, the `on_message` callback is called every time you receive a message on your MQTT topic. In our
case this will be the raw ZigBee data encoded as a JSON object. [This GIST](
https://gist.github.com/ndfred/b373eeafc4f5b0870c1b8857041289a9) has a good summary of the values that are available, so I
won't repeat them here. The details for the electricity meter are included under `elecMtr` then `0702`. There are a series
of values for daily, weekly and monthly usage, but the most useful is the raw meter reading. We can extract this like so:

```python
elec_multiplier = int(elecMtr["03"]["01"], 16)
elec_divisor = float(int(elecMtr["03"]["02"], 16))
elec_meter = int(elecMtr["00"]["00"], 16)

electricity_meter = elec_meter * elec_multiplier / elec_divisor
```

The raw meter reading sent a hex encoded integer, which is scaled by the given multiplier and divisor. Why it's like that
I'm not really sure, but I do appreciate Glow providing as low level data as they can, even if it requires us to deal with
some oddities like this. Once you've decoded and scaled the meter reading we can expose the 

![Electricity Usage](/assets/electricity_usage.png)

![Gas Usage](/assets/gas_usage.png)
