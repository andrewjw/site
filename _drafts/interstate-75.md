---
layout: post
title: Pimoroni's Interstate 75
date: 2023-12-07
tags: hardware
permalink: "/2024/01/01/pimoroni-interstate-75/"
---
I've previously written about my attempts to get metrics about my house into Prometheus
and to visualise them with Grafana. This project has gone well, and I can measure
everything I want to apart from water usage - please let me know in the comments if you
have a suggestion on how to do that! The one thing that's missing is a "glanceable"
display. My Grafana dashboards work really well when I'm at my computer, but not so great
when I'm cooking in the kitchen.

<<<insert grafana screenshot>>>

To solve this I purchased an (Interstate 75W from Pimoroni)[https://shop.pimoroni.com/products/interstate-75?variant=39443584417875],
and a 64x64 2.5mm pitch LED matrix panel.  This is a (Raspberry Pi Pico W)[https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html],
with some additional software and hardware to make driving LED matrix panels easy. The Pico W
contains an (RP2040)[https://www.raspberrypi.com/products/rp2040/specifications/] processor,
264kB RAM and 2MB of flash memory, a USB port and wifi/bluetooth support.

Assembling the panel is easy as the board slots into a space on the panel easily, and connects
with a couple of provided wires. Just don't forget to connect the power cable as well as the
data cable (as I did), as it powers up but the colours look very strange and you'll be confused
for a while.

Getting started with the board is straightforward as (Pimoroni provide an excellent guide)[https://learn.pimoroni.com/article/getting-started-with-interstate-75],
and a custom version of (MicroPython)[https://micropython.org/] with some baked-in
extra libraries to make drawing on the display straightforward. It was only a matter of a few
minutes after unboxing before I had something appearing on the panel.

The additional libraries have a lot of useful functionality, like drawing lines and shapes,
images, text, etc. However, I quickly discovered that the development process was not quite
as slick as I would like. There's no way to run your code on your PC - it will only run on
the physical hardware. Given I would like to mount the panel in my kitchen, having to plug
it in every time I wanted to work on change was going to be impractical.

Partly to solve that inconvenience, and partly because I don't like to make things easy on myself,
I decided to build my own library, (i75)[https://github.com/andrewjw/i75]. This builds on top of
Pimoroni's MicroPython libraries, but only uses the ability to set individual pixels. It also 
abstracts the Interstate 75 away, so when running on a PC it mimics the panels using 
(PyGame)[https://www.pygame.org/].

<<<insert screenshot>>

This approach has several problems, in particular, it runs on Python3 which MicroPython attempts
to replicate, but the standard library is very different. The Pimoroni's build of MicroPython only
emulates single precision floating point numbers, which caused me some trouble when drawing an
analogue clock. And of course, the speed of a PC is about a zillion times quicker than the RP2040,
and has essentially no memory limit. Ideally, in future, I'd like to switch to the PC MicroPython build,
but for now, the simplicity of using PyGame wins out. I've managed to develop the glanceable display
without using the physical hardware, so as long as you keep these limitations in mind it seems to work
ok.

As I write this I have not yet implemented all the displays I wanted to, but it does display the time,
some bouncing balls (mostly as a test of speed) and the album art from whatever's displaying on my
Kitchen (Sonos)[https://www.sonos.com/].

<<insert album art screenshot)

To further improve the speed of development, and to work around the memory and processor limitations
the display has a (frontend)[https://github.com/andrewjw/smartdisplay-frontend] and (backend)[https://github.com/andrewjw/smartdisplay-backend]
component. 
