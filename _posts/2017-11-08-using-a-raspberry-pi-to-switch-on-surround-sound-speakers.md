---
layout: post
title: Using A Raspberry Pi To Switch On Surround Sound Speakers
date: 2017-11-08 12:00:00.000000000 +00:00
type: post
parent_id: '0'
published: true
password: ''
status: publish
categories: []
tags:
- edid
- hdmi
- linux
- mythtv
- onkyo
- raspberrypi
meta:
  _rest_api_published: '1'
  _rest_api_client_id: "-1"
  _publicize_job_id: '11216785275'
  _publicize_done_external: a:1:{s:7:"twitter";a:1:{i:8887;s:56:"https://twitter.com/andrew_j_w/status/928233896852033536";}}
  _publicize_done_10916: '1'
  _wpas_done_8887: '1'
  publicize_twitter_user: andrew_j_w
author:
  login: andrewjw
  email: andrewjwilkinson@gmail.com
  display_name: Andrew Wilkinson
  first_name: Andrew
  last_name: Wilkinson
permalink: "/2017/11/08/using-a-raspberry-pi-to-switch-on-surround-sound-speakers/"
---
<a href="https://www.flickr.com/photos/116606332@N02/15082864407/"><img style="float:right;margin:5px;" src="{{ site.baseurl }}/assets/15082864407_aa13b040d3_m.jpg" alt="Speaker" /></a>In a <a href="https://andrewwilkinson.wordpress.com/2017/10/25/network-booting-a-raspberry-pi-mythtv-frontend/">previous post</a>, I talked about network booting a Raspberry Pi MythTV frontend. One issue that I had to solve was how to turn on my <a href="http://amzn.to/2hIejJl">Onkyo surround sound speakers</a>, but only if they are not already turned on.n
I already had an <a href="https://www.mythtv.org/wiki/MCE_Remote">MCE remote and receiver</a> which can both transmit and receive, so it is perfect for controlling MythTV and switching the speakers on. There are plenty of tutorials out there, but the basic principle is to use <tt>irrecord</tt> to record the signals from the speaker's remote control, so the Raspberry Pi can replay them to switch it on when the Pi starts up. In my case, I needed two keys, the power button and VCR/DVR input button. Once you've recorded the right signals, you can use <tt>irsend</tt> to repeat them.n
Initially, I had it set up to always send the power button signal on boot. This had the unfortunate side-effect of switching the speakers off if they were already on, for example, if I had been listening to music through Sonos before deciding to watch TV.n
To prevent this from happening I needed to determine whether the speakers were on or not. Fortunately, Raspberry Pi's come with some useful tools to determine information about what is supported by the HDMI device it's connected to. These tools are <tt>tvservice</tt>, which dumps the <a href="https://en.wikipedia.org/wiki/Extended_Display_Identification_Data">EDID</a> information, and <tt>edidparser</tt> which turns the EDID into human-readable text.n
You can use them as follows:n
<pre>tvservice -d /tmp/edid.dump

edidparser /tmp/edid.dump &gt; /tmp/edid.txt</pre>
This gives you a nice text file containing all of the resolutions and audio formats supported by the connected HDMI device. I took one output when the speakers were on, and one when they were off, and by <tt>diff</tt>ing them I got this set of changes.n
<pre>-HDMI:EDID found audio format 2 channels PCM, sample rate: 32|44|48 kHz, sample size: 16|20|24 bits
+HDMI:EDID found audio format 2 channels PCM, sample rate: 32|44|48|88|96|176|192 kHz, sample size: 16|20|24 bits
+HDMI:EDID found audio format 6 channels PCM, sample rate: 32|44|48|88|96|176|192 kHz, sample size: 16|20|24 bits
+HDMI:EDID found audio format 8 channels AC3, sample rate: 32|44|48 kHz, bitrate: 640 kbps
+HDMI:EDID found audio format 8 channels DTS, sample rate: 44|48 kHz, bitrate: 1536 kbps
+HDMI:EDID found audio format 6 channels One Bit Audio, sample rate: 44 kHz, codec define: 0
+HDMI:EDID found audio format 8 channels Dobly Digital+, sample rate: 44|48 kHz, codec define: 0
+HDMI:EDID found audio format 8 channels DTS-HD, sample rate: 44|48|88|96|176|192 kHz, codec define: 1
+HDMI:EDID found audio format 8 channels MLP, sample rate: 48|96|192 kHz, codec define: 0</pre>
Pretty obvious really - when the speakers are on they support a much greater range of audio formats!n
Putting all this together I ended up with the following script. It grabs the EDID data, converts it into text, and if it doesn't contain DTS-HD then turn the speakers on.n
<pre>tvservice -d /tmp/edid.dump

edidparser /tmp/edid.dump &gt; /tmp/edid.txt

if ! grep DTS-HD /tmp/edid.txt; then
 irsend SEND_ONCE speaker KEY_POWER
fi</pre>
<hr />
Photo of <a href="https://www.flickr.com/photos/116606332@N02/15082864407/">Speaker</a> by <a href="https://www.flickr.com/photos/116606332@N02/">Ryann Gibbens</a>.n
