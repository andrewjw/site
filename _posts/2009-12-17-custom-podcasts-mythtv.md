---
layout: post
title: Custom Podcasts With MythTV
date: 2009-12-17 13:31:03.000000000 +00:00
type: post
tags:
- bbc
- itunes
- mythtv
- podcast
permalink: "/2009/12/17/custom-podcasts-mythtv/"
---
I love listening to both BBC Radio 4 and BBC 6 Music. Like the rest of the BBC radio stations a significant proportion of the shows are available as a podcast. Unfortunately this is not true of all the shows, and for those that feature music such as Adam &amp; Joe or Steve Lamacq the podcasts are talking only.

I watch almost all of TV through MythTV which records all of my favourite shows automatically while on my way to work I like to listen to podcasts that are downloaded automatically by iTunes. Would it be possible to automatically record shows with MythTV that aren't available as podcasts and sync them to my iPhone automatically?

Recording a radio show with MythTV is no different to recording a TV show so that's not a problem. MythTV also provides the ability to run a script after certain shows have been recorded. All that is required is a script that converts the recording into an mp3 file and to build an RSS feed which can be read by iTunes.

First we need to convert the recorded file into an mp3, which is easy to do with the ffmpeg program.

    #!/usr/bin/python
    # -*- coding: utf-8 -*-

    from datetime import date, datetime
    import glob
    import MySQLdb
    import os
    import sys

    input = sys.argv[1]
    input_filename = input.split("/")[-1]
    output_filename = input_filename.split(".")[0] + ".mp3"

    os.system("ffmpeg -y -i %s -acodec libmp3lame -ab 128k /var/www/localhost/htdocs/podcasts/%s &gt; /dev/null" % (input, output_filename))

Next up we need write out the RSS feed that iTunes will read. We start off by opening the file and writing out some boiler plate code.

    fp = open("/var/www/localhost/htdocs/podcasts/feed.rss", "w")
    fp.write("""&lt;?xml version="1.0" encoding="UTF-8"?&gt;

    &lt;rss xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" version="2.0"&gt;
      &lt;channel&gt;
           &lt;title&gt;MythTV Recorded Radio&lt;/title&gt;
           &lt;description&gt;Radio Recorded By MythTV&lt;/description&gt;
           &lt;link&gt;http://192.168.0.8/podcasts/&lt;/link&gt;
           &lt;language&gt;en-us&lt;/language&gt;
           &lt;lastBuildDate&gt;%(datetime)s&lt;/lastBuildDate&gt;
           &lt;pubDate&gt;%(datetime)s&lt;/pubDate&gt;
           &lt;webMaster&gt;andrewjwilkinson@gmail.com&lt;/webMaster&gt;

           &lt;itunes:image href="http://192.168.0.8/podcasts/stevelamacq.jpg"/&gt;

           &lt;itunes:category text="Technology"&gt;
               &lt;itunes:category text="Podcasting"/&gt;
           &lt;/itunes:category&gt;
    """ % { "datetime": datetime.now().ctime() })

Finally we need to write out a small bit of XML for each file that's in our directory waiting to be downloaded. We do this by looking at each mp3 file in the podcasts directory and looking for the appropriate entry in MythTV's `recorded` table. If an entry doesn't exist then recording has been deleted and we delete the mp3 file.

    db = MySQLdb.connect(user="mythtv", passwd="mythtv", db="mythconverg")

    for radio_file in glob.glob("/var/www/localhost/htdocs/podcasts/*.mp3"):
        output = radio_file.split("/")[-1]
        size = len(open(radio_file, "rb").read())

        c = db.cursor()
        c.execute("SELECT title, description, starttime FROM recorded WHERE basename=%s", (output.split(".")[0] + ".mpg", ))
        row = c.fetchone()
        if row is None:
            os.remove(radio_file)
            continue

        title, description, starttime = row

        fp.write("""       &lt;item&gt;
               &lt;title&gt;%(title)s - %(datetime)s&lt;/title&gt;
               &lt;link&gt;http://192.168.0.8/podcasts/%(output)s&lt;/link&gt;
               &lt;guid&gt;http://192.168.0.8/podcasts/%(output)s&lt;/guid&gt;
               &lt;description&gt;%(description)s&lt;/description&gt;
               &lt;enclosure url="http://192.168.0.8/podcasts/%(output)s" length="%(output_size)s" type="audio/mpeg"/&gt;
               &lt;category&gt;Podcasts&lt;/category&gt;
               &lt;pubDate&gt;%(datetime)s&lt;/pubDate&gt;
           &lt;/item&gt;""" % { "title": title, "description": description, "datetime": starttime, "output": output, "output_size": size })

    fp.write("""
        &lt;/channel&gt;
    &lt;/rss&gt;
    """)

To use this put all three bits of code into one file, save it somewhere and mark it as executable. Next set up Apache to serve the directory `/var/www/localhost/htdocs/podcasts/` as `/podcasts`. Finally you need to set up the script to run automatically after a program you want to create a podcast from has been recorded. To do this run `mythtv-setup` and select the 'general' menu option. Move through the screens until you reach 'Job Queue (Job Commands)'. Add a brief description of the script in the 'description' field then enter the `&lt;path to script&gt; %s`. Then use the normal MythTV frontend and edit the recording schedules to make the correct User Script run.

Point iTunes at `http://you.ip.address/podcasts/feed.rss` and it'll automatically download any new recordings.
