---
title: Router Stats To Prometheus
layout: post
---
I've previously written about my plan to collect much more data about my house. In the current work-from-home
environment the quality of our internet connection is paramount, and I wanted to be able to monitor it and
potentially be alerted to any degradation before it becomes an issue.

Although I've replaced my wifi with a [UniFi](https://unifi-network.ui.com/) based system, I still use the router
that was supplied by my [ISP](https://www.zen.co.uk/broadband) - which is a [ZyXEL VMG1312-B10D](
https://www.zyxel.com/uk/en/products_services/Wireless-N-VDSL2-4-port-Gateway-with-USB-VMG1312-B10D/). Like most
networking equipment the ZyXel supports [SNMP](https://en.wikipedia.org/wiki/Simple_Network_Management_Protocol)
which is a technology for reading and writing stats and configuration from equipment, and aggregating them together.
On paper it sounds great, but unfortunately SNMP is a nightmare to work with, and you need a mapping file for each
device, which doesn't exist for my device. After looking into creating this mapping, and integrating my preferred
technology slack of [Grafana](https://grafana.com/) and [Prometheus](http://prometheus.io/), I decided to change tack
and extract the data myself.

Fortunately the route UI contains some plain text data which looks easy to scrape. So, filled with confidence that
this would be an easier approach that learning SNMP I spun up a [GitHub project](
https://github.com/andrewjw/zyxelprometheus) and got to work cranking out some code.

```plain

============================================================================
    VDSL Training Status:   Showtime
                    Mode:   VDSL2 Annex B
            VDSL Profile:   Profile 17a
                G.Vector:   Disable
            Traffic Type:   PTM Mode
             Link Uptime:   1 day: 4 hours: 28 minutes
============================================================================
       VDSL Port Details       Upstream         Downstream
               Line Rate:      7.881 Mbps       39.998 Mbps
    Actual Net Data Rate:      7.853 Mbps       39.999 Mbps
          Trellis Coding:         ON                ON
              SNR Margin:        5.7 dB            7.3 dB
            Actual Delay:          0 ms              0 ms
          Transmit Power:      - 2.6 dBm          11.4 dBm
           Receive Power:      -20.8 dBm         -11.0 dBm
              Actual INP:        0.0 symbols      55.0 symbols
       Total Attenuation:       18.2 dB           22.4 dB
Attainable Net Data Rate:      7.853 Mbps       47.093 Mbps
============================================================================
      VDSL Band Status    U0      U1      U2      U3      D1      D2      D3
  Line Attenuation(dB):  7.2    40.1     N/A     N/A    18.1    50.3    77.6
Signal Attenuation(dB):  7.2    39.9     N/A     N/A    20.0    50.1     N/A
        SNR Margin(dB):  5.5     5.7     N/A     N/A     7.3     7.3     N/A
   Transmit Power(dBm):-13.7   - 3.0     N/A     N/A     8.9     7.8     N/A
============================================================================
```

The first step to implement this was to investigate how the built in UI requests this data. An early discovery
was that when accessing using HTTP responses are encrypted with AES and then decrypted in Javascript. When
accessing with HTTPS (which uses a self-signed ZyXEL certificate) responses are in plain text.

Unfortunately, but perhaps not unsurprisingly, at this point I hit what appears to be a bug in the router.
The stats work well for a few hours, but then the router stopped responding. Even more strangely after this
occurs it was impossible to log in manually to the web UI - the router responded with a username or password
is not valid error. Seemly the only solution was to reboot the router. Extending the Prometheus scrape interval
extended the time that the stats worked for, but eventually the same error reoccurred.