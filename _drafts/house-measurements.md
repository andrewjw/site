---
title: House Measurements
layout: post
---
For a long time now I've tracked the weather outside my house with my [weather station](https;//www.welynweather.co.uk). I also
have smart electric and gas meters which display my usage on a little screen in my kitchen, but I didn't tried to do anything
useful with that data. Recently I brought an electric car, and given that it's basically a giant iPad on wheels it inspired me
to look into what data I could collect from it, and from elsewhere in my house.

Towards the end of last year I upgraded my [Synology NAS](https://www.synology.com/en-uk) to a newer model which has an Intel,
rather than MIPS processor, partly because it was old and I was worried about it dying, but mostly so I could run Docker containers
on it. I've been running both a [Ubiquiti UniFi Controller](https://www.ui.com/software/) and [PiHole](https://pi-hole.net/) since then,
but I knew as part of this project I'd want to run many more containers so I took the opportunity to tidy up the set up.

Docker Compose is a tool which sits above the normal `docker` command and it lets you run multiple docker containers, while simplifying
the management of images and the options you need to set for the container to work correctly. You can find my `docker-compose.yml` file
[here](https://github.com/andrewjw/docker).

At [work](https://www.ocadotechnology.com/) we make extensive use of [Prometheus](https://prometheus.io/) from recording our metrics
and [Grafana](https://grafana.com/) to display them, so they were the obvious choice for my home monitoring as well. Both are incredibly
easy to set up, with Docker containers already available.

One key metric I knew I needed to track was the amount of free space on my NAS. I'm a long time [MythTV](https://www.mythtv.org/) user,
and my kids record vast quantities of [Hey Duggee](https://www.heyduggee.com/) which I need to keep an eye on. Fortunately the Prometheus
team make this easy by providing [`node-exporter`](https://github.com/prometheus/node_exporter), which produces all the metrics you might
want to monitor a server, including disk space. If you run it inside Docker then by default it will give you stats from inside the container,
but by mounting some key directories inside the container you can get metrics for the whole machine.

```yaml
  node-exporter:
    privileged: true
    image: prom/node-exporter:v1.0.1
    container_name: node-exporter
    restart: always
    network_mode: host
    ports:
      - 9100:9100
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
      - /volume1:/volume1:ro
    command:
      - "--log.level=debug"
      - "--path.procfs=/host/proc"
      - "--path.sysfs=/host/sys"
      - "--collector.filesystem.ignored-mount-points"
      - "^/(rootfs/)?(dev|etc|host|proc|run|sys|volume1/@docker)($$|/)"
```

Above a certain level, I don't particularly care about the absolute amount of disk space, what really matters is the direction it's trending.
To highlight when I need to look at the amount of TV being recorded I set an alert to trigger when we dropped more than 20Gb of disk space in
a week.
