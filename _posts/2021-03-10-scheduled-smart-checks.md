---
title: Scheduled SMART Checks
layout: post
date: 2021-03-10
tags:
- mac
- smart
permalink: "/2021/03/10/scheduled-smart-checks/"
flickr_user: 'https://www.flickr.com/photos/philipus/'
flickr_username: Philip Dygeus
flickr_image: 'https://live.staticflickr.com/5822/29711988683_96e4c16c23.jpg'
flickr_imagelink: 'https://www.flickr.com/photos/philipus/29711988683'
flickr_imagename: 'Maxtor hard drive'
---
For years hard disks (both spinning rust and SSDs) have had a built in monitoring system that tracks
various metrics about the health of your disk, called [SMART](https://en.wikipedia.org/wiki/S.M.A.R.T.).
In the old days if you were lucky you might get some warning that your disk was about to fail because
it would start to make a nasty noise. In the modern era of SSDs you likely won't get any warning, and
suddenly boom, your laptop won't boot or mount the disk.

Obviously nothing is perfect, and any monitoring can miss a failure, but the potential of some warning
is better than definitely not getting any. Also this is no subtitute for a proper backup and recovery
strategy, but in most home situations people don't have spare laptops or hard drives just sitting around.

It would be relatively easy for operating system vendors to automatically detect SMART capabable drives
and automatically run a check every so often. If it fails, they could pop up a warning about a potential
imminent failure. As far as I know though, no-one does this.
<!--more-->

There is a simple command line tool that lets you interrogate SMART attributes yourself,
[`smartctl`](https://www.smartmontools.org/). It is available in all Linux distribution package repositories,
and in both Homebrew and MacPorts for Mac OS. I'm not a Windows user, so I'm not sure about using it there.

On both my work and my personal MacBooks, and my home Linux server I run something similar to the following.
First I have a script which enables SMART monitoring, then triggers a short test, waits for it to complete
and finally emails me the output.

```bash
#!/bin/bash

/opt/local/sbin/smartctl --all /dev/disk1 -s on

/opt/local/sbin/smartctl --all /dev/disk1 -t short 2>&1 > /dev/null

sleep 600

/opt/local/sbin/smartctl --all /dev/disk1 | /usr/bin/mail -s 'MacBook SMART' myemailaddress
```

On Linux it's easy to use `cron` to trigger this script weekly. On Mac OS it's a [little more complicated](
https://superuser.com/questions/126907/how-can-i-get-a-script-to-run-every-day-on-mac-os-x),
but the following `plist` file will do it. Simple place it in `/Users/username/Library/LaunchAgents/smartctl.plist`
(replacing your username and script file name as appropriate), and it'll get run weekly, when you switch
your laptop on.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
    <dict>
        <key>Label</key>
        <string>smartctl</string>
        <key>Program</key>
        <string>/Users/andrew/bin/smartctl</string>
        <key>StartCalendarInterval</key>
        <dict>
            <key>Hour</key>
            <integer>0</integer>
            <key>Minute</key>
            <integer>0</integer>
            <key>Weekday</key>
            <integer>1</integer>
       </dict>
       <key>AbandonProcessGroup</key>
       <true/>
    </dict>
</plist>
```

On my work laptop `smartctl` is reporting `PASSED`, but one attribute is failing. I guess we just need
to wait and see what happens. Fingers crossed it holds out until I can get Apple-silicon-powered MacBook Pro.

```plain
173 Wear_Leveling_Count     0x0032   096   096   100    Old_age   Always   FAILING_NOW 12309581794157
```
