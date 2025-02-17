---
title: Shelly
---

```
let device = { addr: "192.168.1.65", type: "Switch", id: 0 };

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
