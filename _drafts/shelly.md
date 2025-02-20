---
layout: post
title: Shelly Plug Control
date: 2025-02-13
tags:
  - "smart home"
  - prometheus
  - grafana
permalink: "/2025/02/27/shelly-plug-control/"
---

I've recently become quite interested in the Shelly smart home ecosystem, and I have purchased a few of the (plugs)[https://shellystore.co.uk/product/shelly-plus-plug-uk/] to
play with. One of the key advantages for me is that all processing happens locally, so there is no dependence on a potentially unstable or insecure cloud component.

To save energy I have some devices that I prefer to only be powered when our TV is on. For many years I've used a (powerdown plug)[https://www.amazon.co.uk/Energy-Powerdown-Protection-Remote-EON/dp/B00VKU57D4]
which turns on the TV and peripherals together, and then detects when the TV is turned off and automatically powers down the other devices. It worked very reliably, but as the TV was powered down it made
turned it back on quite slow.

The Shelly plugs have a Javascript interpreter which lets you run scripts to perform custom actions as needed. My idea was to monitor the power level and switch on the peripherals when the
TV power increased, and turn them off when it dropped.

The first step was to visualise the power levels of my TV, which I could do using a (Prometheus exporter)[https://github.com/webdevops/shelly-plug-exporter]. This then allowed me to calibrate the thresholds for switching the peripherals on and off.

!(Graph showing the TV power over time)[/assets/202502_tv_power.png]

The graph shows clear spikes to around 50W while the TV was ok, and one brief spike to 10W while it was off, but the rest of the time it is using less than 1W. I decided that if the TV power went above 20W the peripherals would turn on, if it went below 5W they would turn off, and anywhere in between they would stay in their current state.

The Shelly script API allows you to listen to status updates by calling the (`addStatusHandler`)[https://shelly-api-docs.shelly.cloud/gen2/Scripts/ShellyScriptLanguageFeatures/#shellyaddeventhandler-and-shellyaddstatushandler] function.

```javascript
Shelly.addStatusHandler(check_power);
```

Unfortunately, while the Shelly documentation states that your callback will be called with objects the same as emitted
by (`NotifyStatus`)[https://shelly-api-docs.shelly.cloud/gen2/General/Notifications], the documentation isn't clear
about what those objects will look like. (Elsewhere)[https://shelly-api-docs.shelly.cloud/gen2/ComponentsAndServices/Switch#status]
the status objects are described though, so with a combination of documentation and some good ol' `console.log` debug I was able
to work out that `msg.delta.apower` (Active Power) would contain the current power draw on my TV.

```javascript
let current_status = "off";

function check_power(msg) {
  if (!def(msg.delta) || !def(msg.delta.apower)) return;

  let current_power = msg.delta.apower;

  if (current_power > 20 && current_status != "on") {
    turn("on")
  } else if (current_power < 5 && current_status != "off") {
    turn("off")
  }
}
```

To control the slave plug we just need to 

```javascript
let device = { addr: "<slave plug IP address>", type: "Switch", id: 0 };

function turn(dir) {
  on = dir == "on" ? "true" : "false";

  let cmd = "rpc/" + device.type + ".Set?id=" + device.id.toString() + "&on=" + on;
  Shelly.call("HTTP.GET", { url: "http://" + device.addr + "/" + cmd }, callback);

  current_status = dir;
}
```

For completeness, here is the full script.

```javascript
let device = { addr: "<slave plug IP address>", type: "Switch", id: 0 };

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
