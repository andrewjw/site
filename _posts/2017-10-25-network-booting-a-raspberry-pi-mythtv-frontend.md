---
layout: post
title: Network Booting A Raspberry Pi MythTV Frontend
date: 2017-10-25 12:00:37.000000000 +01:00
type: post
parent_id: '0'
published: true
password: ''
status: publish
categories: []
tags:
- mythtv
- raspberrypi
meta:
  _rest_api_published: '1'
  _rest_api_client_id: "-1"
  _publicize_job_id: '10713985870'
  _publicize_done_external: a:1:{s:7:"twitter";a:1:{i:8887;s:56:"https://twitter.com/andrew_j_w/status/923143071746969600";}}
  _publicize_done_10916: '1'
  _wpas_done_8887: '1'
  publicize_twitter_user: andrew_j_w
author:
  login: andrewjw
  email: andrewjwilkinson@gmail.com
  display_name: Andrew Wilkinson
  first_name: Andrew
  last_name: Wilkinson
permalink: "/2017/10/25/network-booting-a-raspberry-pi-mythtv-frontend/"
---
<a href="https://www.flickr.com/photos/jerryjohn/63351338/"><img style="float:right;border:0;" src="{{ site.baseurl }}/assets/63351338_222dc172e1_m.jpg" alt="Network cables - mess :D" /></a>When we moved house earlier in the year I wanted to simplify our home theatre setup. With my son starting to grow up, in a normal house he'd be able to turn on the tv and watch his favourite shows without needing us to do it for him, but with the overcomplicated setup that we had it would take him several years longer before he could learn the right sequence of buttons.n
I've been a <a href="http://www.mythtv.org">MythTV</a> user for well over ten years, and all our TV watching is done through it. At this stage with our history of recorded shows and a carefully curated list of recording rules switching would be a big pain, so I wanted to try and simplify the user experience, even if it means complicating the setup somewhat.n
I had previously tried to reduce the standby power consumption by using an <a href="https://www.amazon.co.uk/dp/B00VKU57D4/ref=cm_sw_r_cp_api_ezg7zb995ZDKJ">Eon Power Down Plug</a>, which monitors the master socket and switches off the slave sockets when the master enters standby mode. This works great as when the TV was off my Xbox and surround speakers would be switched off automatically. The downside is that if I want the use the speakers to listen to music (they are also connected to a <a href="http://amzn.to/2lbf162">Sonos Connect</a>) then either the TV needs to be on, or I need to change the plug over. Lastly, because I was running a combined frontend and backend it wasn't connected to the smart plug (otherwise it wouldn't be able to turn on to record.) If you turned the TV off the frontend would still be on, preventing the backend from shutting down for several hours, until it went into idle mode.n
I decided to solve these problems by using a <a href="http://amzn.to/2ld3GT8">Raspberry Pi 3</a> as a separate frontend, and switching the plugs around. As they run Linux, and have hardware decoding of MPEG2 and h264 they work great as MythTV frontends.n
A common issue with Raspberry Pis is that if you don't shutdown them down correctly then their SD cards become corrupt. If I connected the Pi to the slave plug socket as planned then it would be uncleanly shut down every time the TV was switched off, risking regular corruption. Fortunately Raspberry Pis support network booting, which means you can have the root filesystem mounted from somewhere else, and you don't even need the SD card at all. I already had a <a href="http://www.synology.com">Synology NAS</a>, which I love, and is a perfect host for the filesystem.n
Sadly the network code that is built into the Pis ROM (and therefore isn't updatable) is very specific and buggy. My router's DNS server doesn't support the options required to make the Pi boot, so I switched to using a <a href="https://forum.synology.com/enu/viewtopic.php?t=129075">DNS server on the Synology</a>. While you can't set the right options in the web frontend you can edit the config files directly to make it work. The bugs in the Pis firmware are that the DNS responses must be received at the right time. Too quick or too slow and the Pi will fail to boot. One of the aspects I like the most about my Synology is that it has a very low power suspend more. When it is in this mode it takes a little while to wake up and respond the network event. Waking up takes too long for the Pi, which would give up waiting for a response. While I wouldn't have been happy about it, I could have disabled the low power mode to make the Pi work. Unfortunately the second time the Pi boots the DNS server responds too quickly (the first time it has to check whether the IP address it is about to hand out is in use.) This response is too quick for the Pi, which again will fail to boot.n
The other option is to use an SD card with a kernel and a few supporting files on it to start the boot, and then use Linux's built-in NFS root filesystem support. While this does require an SD card, it's read only and after the kernel has been loaded the card will be accessed very rarely, if ever, so the risk of corruption is minimal. After running with this set up for a few months, and being switched off several times per day we've not had a single corruption of the SD card so far.n
Setting this up is pretty straightforward, I just extracted a Minibian tarball to my NAS and shared it via NFS. Next I copied the contents of /boot to my SD card, and modified cmdline.txt to include the following:n
<pre>root=/dev/nfs nfsroot=192.168.1.72:/volume1/pi/minibian rw ip=dhcp</pre>
With this added it boots up reliably and can be shut down uncleanly with little or no risk of corruption.n
Next up is making the MythTV frontend start up automatically. This is was done by adding the following to /etc/rc.localn
<pre>modprobe rc_rc6_mce
/usr/bin/ir-keytable -c -p RC-5,RC-6 -w /etc/rc_keymaps/rc6_mce
echo "performance" &gt; /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
su -c "/home/andrew/autostart.sh" andrew &amp;</pre>
The first two lines are required to set up my MCE IR receiver. The third line is needed to ensure that the Pi's performance remains consistent and the CPU isn't throttled down while you're in the middle of an episode of Strictly. The final line just triggers another script that actually runs the frontend, but run as me, and not root.n
<pre>#!/bin/bash

/home/andrew/wake_speakers &amp;
startx /home/andrew/start_myth 2&gt;&amp;1 &gt; ~/mythtv.log</pre>
I'll cover the first line in another post, but it just turns on the surround speakers and makes sure they in the right mode. The second line starts X, and runs my custom start script. This final script looks like this:n
<pre>#!/bin/bash
QT_QPA_PLATFORM=xcb /usr/bin/mythfrontend -O libCECEnabled=0</pre>
While I managed to solve my key issues of making it easier to switch the open and off, and I can listen to music without the TV being on and still have most devices switched fully off, I still have a few issues still to solve. The main two are that bootup speed is not as fast as I would like, and the backend doesn't cope well with the frontend exiting uncleanly (and it waits 2.5 hours before turning off). I will cover these issues, and some others that I had to solve in a future post.n
<hr />
Photo of <a href="https://www.flickr.com/photos/jerryjohn/63351338/">Network cables - mess :D</a> by <a href="https://www.flickr.com/photos/jerryjohn/">jerry john</a>.n
Links to Amazon contain an affiliate code.n
