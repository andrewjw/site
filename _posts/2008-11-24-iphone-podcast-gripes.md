---
layout: post
title: iPhone podcast gripes
date: 2008-11-24 13:31:13
tags: podcasts iphone apple
permalink: "/2008/11/24/iphone-podcast-gripes/"
---
I've been using my iPhone for two weeks now, and overall it's great. Easily the best phone I've ever used.
It really has changed the way I live my life because there is so much I can now do from anywhere that
before I'd need to be at my computer for.

Despite this though, there are a few things that Apple should fix.

1. **There's no character count when typing a text message**.
 This might be a small issue and given I get 500 free texts a month (which is way more than I use) it doesn't
 matter that I might sometimes send people two messages. However, it would be nice to be able tailor my
 messages to the limit of 160 characters.
1. **The new over-the-air download of podcasts is completely broken.**

Rather than listen to my music on a loop while I travel I listen to a number of podcasts,
and Steve Lamacq's 6music show. MythTV on my PC records his show every afternoon. A script
then converts the recording into a 300MB MP3 file and updates the xml document that describes
it as a podcast. This is served by Apache on my local machine.
<!--more-->

Specifying `http://192.168.0.8/podcasts/feed.rss` works fine for iTunes on my PC. When I sync my
iPhone new episodes of Lamacq's show get copied automatically across.

It was well known that an update last week would add over the air downloads for podcasts. This
would be brilliant I thought, because then I wouldn't need to turn my girlfriends laptop on
unless I want to back my phone up.

Disappointingly there are two big flaws with the implementation of podcasts on the phone when
compared to podcasts on iTunes. Firstly there is no automatic checking for new episodes - you
must press a button for each feed to see if it has been updated. Secondly only podcasts that
are delivered through the iTunes store can be downloaded straight to your phone. When attempting
to sync my custom podcast on my phone no attempt is made to download the feed and I get sent to
the store's podcast homepage.

Is there any need for this limitation? I can't think of a good reason for it :-(

Google is useless to see if anyone else has come across this issue or resolved it because it's
full of speculation and screenshots from before the update was released.
