---
layout: post
title: Last.fm Chart Changes
date: 2009-05-28T11:16:08.000Z
type: post
tags:
  - chart changes
  - firefox
  - greasemonkey
  - lastfm
permalink: /2009/05/28/last-fm-chart-changes/
---
For several years I've written and maintained a
[GreaseMonkey](https://addons.mozilla.org/en-US/firefox/addon/748) script which adds chart change information
to your music charts. The biggest problem with a greasemonkey script is that you don't control the page you're
modifying. Last week, for the umpteenth time, Last.fm changed their page again and broke the script.

Fortunately, I've fixed the script and have taken the opportunity to improve the webservice that it uses. This
means that the charts should be more cachable to improve performance for you and reducing bandwidth usage for
me. I've also added support for weekly charts so they'll now have chart change information, as they used to
before Last.fm's most recent redesign removed it.

Finally, because my host [Linode.com](http://www.linode.com) recently increased the disk space on all their
plans by a third, I'm able to increase the length of time all charts are stored for 30 to 120. Unfortunately
as I had to delete all the chart change information you won't see a change initially but gradually you'll see
your charts are available for longer and longer.

You can download the updated script [here](http://lastfm.indiegigs.co.uk/chartchanges).

Enjoy!
