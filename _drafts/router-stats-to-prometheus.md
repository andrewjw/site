---
title: Router Stats To Prometheus
---
ZyXEL VMG1312-B10D

When accessing by HTTP responses are encrypted with AES and then decrypted in Javascript. When accessing with
HTTPS (which uses a self-signed ZyXEL certificate) responses are in plain text.

Unfortunately, but perhaps not unsurprisingly, at this point I hit what appears to be a bug in the router.
The stats work well for a few hours, but then the router stopped responding. Even more strangely after this
occurs it was impossible to log in manually to the web UI - the router responded with a username or password
is not valid error. Seemly the only solution was to reboot the router. Extending the Prometheus scrape interval
extended the time that the stats worked for, but eventually the same error reoccurred.