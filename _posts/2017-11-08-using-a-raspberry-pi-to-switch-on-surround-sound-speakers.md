---
layout: post
title: Using A Raspberry Pi To Switch On Surround Sound Speakers
date: 2017-11-08 12:00:00.000000000 +00:00
tags:
- edid
- hdmi
- linux
- mythtv
- onkyo
- raspberrypi
permalink: "/2017/11/08/using-a-raspberry-pi-to-switch-on-surround-sound-speakers/"
flickr_user: 'https://www.flickr.com/photos/116606332@N02/'
flickr_username: Ryann Gibbens
flickr_image: 'https://live.staticflickr.com/3840/15082864407_aa13b040d3_w.jpg'
flickr_imagelink: 'https://www.flickr.com/photos/116606332@N02/15082864407/'
flickr_imagename: 'Speaker'
---
In a [previous post](/2017/10/25/network-booting-a-raspberry-pi-mythtv-frontend/")
, I talked about network booting a Raspberry Pi MythTV frontend. One issue that I had to solve was how
to turn on my [Onkyo surround sound speakers](http://amzn.to/2hIejJl), but only if they are not
already turned on.

I already had an [MCE remote and receiver](https://www.mythtv.org/wiki/MCE_Remote) which can both
transmit and receive, so it is perfect for controlling MythTV and switching the speakers on. There are plenty
of tutorials out there, but the basic principle is to use `irrecord` to record the signals from the
speaker's remote control, so the Raspberry Pi can replay them to switch it on when the Pi starts up. In my
case, I needed two keys, the power button and VCR/DVR input button. Once you've recorded the right signals,
you can use `irsend` to repeat them.

Initially, I had it set up to always send the power button signal on boot. This had the unfortunate
side-effect of switching the speakers off if they were already on, for example, if I had been listening to
music through Sonos before deciding to watch TV.
<!--more-->

To prevent this from happening I needed to determine whether the speakers were on or not. Fortunately,
Raspberry Pi's come with some useful tools to determine information about what is supported by the HDMI device
it's connected to. These tools are `tvservice`, which dumps the
[EDID](https://en.wikipedia.org/wiki/Extended_Display_Identification_Data) information, and
`edidparser` which turns the EDID into human-readable text.

You can use them as follows:

```bash
tvservice -d /tmp/edid.dump

edidparser /tmp/edid.dump > /tmp/edid.txt
```

This gives you a nice text file containing all of the resolutions and audio formats supported by the connected
HDMI device. I took one output when the speakers were on, and one when they were off, and by `diff`ing
them I got this set of changes.

```plain
    -HDMI:EDID found audio format 2 channels PCM, sample rate: 32|44|48 kHz, sample size: 16|20|24 bits
    +HDMI:EDID found audio format 2 channels PCM, sample rate: 32|44|48|88|96|176|192 kHz, sample size: 16|20|24 bits
    +HDMI:EDID found audio format 6 channels PCM, sample rate: 32|44|48|88|96|176|192 kHz, sample size: 16|20|24 bits
    +HDMI:EDID found audio format 8 channels AC3, sample rate: 32|44|48 kHz, bitrate: 640 kbps
    +HDMI:EDID found audio format 8 channels DTS, sample rate: 44|48 kHz, bitrate: 1536 kbps
    +HDMI:EDID found audio format 6 channels One Bit Audio, sample rate: 44 kHz, codec define: 0
    +HDMI:EDID found audio format 8 channels Dobly Digital+, sample rate: 44|48 kHz, codec define: 0
    +HDMI:EDID found audio format 8 channels DTS-HD, sample rate: 44|48|88|96|176|192 kHz, codec define: 1
    +HDMI:EDID found audio format 8 channels MLP, sample rate: 48|96|192 kHz, codec define: 0
```

Pretty obvious really - when the speakers are on they support a much greater range of audio formats!

Putting all this together I ended up with the following script. It grabs the EDID data, converts it into text,
and if it doesn't contain DTS-HD then turn the speakers on.

```bash
tvservice -d /tmp/edid.dump

edidparser /tmp/edid.dump > /tmp/edid.txt

if ! grep DTS-HD /tmp/edid.txt; then
 irsend SEND_ONCE speaker KEY_POWER
fi
```
