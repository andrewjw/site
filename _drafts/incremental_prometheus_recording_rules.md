---
layout: post
title: Incremental Prometheus Recording Rules
date: 2024-02-01
tags: prometheus
permalink: "/2024/03/01/incremental-prometheus-recording-rules/"
---

Incremental Prometheus Recording Rules.

```
+ on () ((octopus_standing{type='electric'} and on () (hour()==0 and minute()==0)) or vector(0))
```
