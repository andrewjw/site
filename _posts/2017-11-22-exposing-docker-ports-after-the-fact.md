---
layout: post
title: Exposing Docker Ports After The Fact
date: 2017-11-22 12:00:50.000000000 +00:00
tags:
- port forwarding
- socat
- docker
permalink: "/2017/11/22/exposing-docker-ports-after-the-fact/"
flickr_user: 'https://www.flickr.com/photos/mireia/'
flickr_username: Mireia mim
flickr_image: 'https://live.staticflickr.com/185/415518987_a193159cdd_w.jpg'
flickr_imagelink: 'https://www.flickr.com/photos/mireia/415518987/'
flickr_imagename: 'Almacenaje Colorido'
---
[Docker](http://www.docker.com) is a great tool for running your applications in a consistent and
repeatable environment. One issue that I've come across occasionally is getting data into and out of the
environment when it's running.

In this post I want to talk about exposing ports that are published by applications running inside a
container. When you start up the container it's pretty easy to configure the ports you want to expose using
the `--publish` or `-p` parameter. It's followed by the internal port number, a colon, and the
external port number. For example:

`docker run --publish 80:8080 myapp`

This will publish port 80 from inside the container as port 8080 on the host.

This works great if you know want ports you want to expose before you run the container. Once it's running,
if you decide you need access to a port, you can't expose it. Unless that is, you cheat.
<!--more-->

[socat](https://linux.die.net/man/1/socat) is a very useful command line tool which lets
you create tunnels to forward ports. It has many other features, such as forwarding unix sockets to tcp
sockets, but we just need to forward a port from an existing container, into a new container and then expose
that port to the host.

Fortunately a Docker container that's only job is to run `socat` already exists, so we just need to
pass the right options to forward the remote port, and expose the port.

I was trying to expose port 61616 from a container called `activemq`, so I ran the following command:

```bash
docker run -p 61616:61616 alpine/socat tcp-listen:61616,reuseaddr,fork tcp:activemq:61616
```

Let's break the command down.

`docker run -p 61616:61616`

This runs the container and exposes port 61616 on port 61616 on the host.

`alpine/socat`

This runs the container alpine/socat.

`tcp-listen:61616,reuseaddr,fork`

This is the first parameter that's passed to socat. It specifies that it should listen on port 61616.

`tcp:activemq:61616`

This specifies that when an incoming connection arrives it should be connected port 61616 running on container activemq.

So to summarise, you can run the following command and expose a port while a container is running.

```bash
docker run -p cport:hostport alpine/socat tcp-listen:cport,reuseaddr,fork tcp:remotehost:remoteport
```
