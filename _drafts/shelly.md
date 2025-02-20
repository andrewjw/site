---
layout: post
title: Shelly Plug Control
date: 2025-02-13
tags: "smart home" prometheus grafana
permalink: "/2025/02/27/shelly-plug-control/"
---

I've recently become quite interested in the Shelly smart home ecosystem, and I have purchased a few of the (plugs)[https://shellystore.co.uk/product/shelly-plus-plug-uk/] to
play with. One of the key advantages for me is that all processing happens locally, so there is no dependence on a potentially unstable or insecure cloud component.

To save energy I have some devices that I prefer to only be powered when our TV is on. For many years I've used a (powerdown plug)[https://www.amazon.co.uk/Energy-Powerdown-Protection-Remote-EON/dp/B00VKU57D4]
which turns on the TV and peripherals together, and then detects when the TV is turned off and automatically powers down the other devices. It worked very reliably, but as the TV was powered down it made
turned it back on quite slow.

The Shelly plugs have a Javascript interpreter which lets you run scripts to perform custom actions as needed. My idea was to monitor the power level and switch on the peripherals when the
TV power increased, and turn them off when it dropped.

The first step was to visualise the power levels of my TV, which I could do using a (Prometheus exporter)[https://github.com/webdevops/shelly-plug-exporter]. This the allowed by to
calibrate the thresholds for switching the peripherals on and off.

```
let device = { addr: "<slave plug IP address)", type: "Switch", id: 0 };

let current_status = "off";

function callback(result, error_code, error_message) {
  if (error_code != 0) {
    print("fail");
  } else {
    print("success");
  }
}

function turn(dir) {
  on = dir == "on" ? "true" : "false";

  let cmd = "rpc/" + device.type + ".Set?id=" + device.id.toString() + "&on=" + on;
  Shelly.call("HTTP.GET", { url: "http://" + device.addr + "/" + cmd }, callback);

  current_status = dir;
}

function check_power(msg) {
  if (!def(msg.delta) || !def(msg.delta.apower)) return;

  let current_power = msg.delta.apower;
  console.log(current_power);

  if (current_power > 20 && current_status != "on") {
    turn("on")
  } else if (current_power < 5 && current_status != "off") {
    turn("off")
  }
}

function def(o) {
  return typeof o !== "undefined";
}

Shelly.addStatusHandler(check_power);
```
