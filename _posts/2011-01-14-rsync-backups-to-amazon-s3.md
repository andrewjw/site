---
layout: post
title: Rsync backups to Amazon S3
date: 2011-01-14 12:40:01.000000000 +00:00
type: post
parent_id: '0'
published: true
password: ''
status: publish
categories:
- unix
tags:
- amazon
- backup
- linux
- rsync
- s3
- trickle
meta:
  _edit_last: '364050'
  _wpas_done_twitter: '1'
  _oembed_96bbe51a4c27ad0d5e7dd8026beec5df: "{{unknown}}"
  _oembed_e2f28713d5a36f5fbd3b0d2bd903a253: "{{unknown}}"
  _oembed_b4f34d32ba2f47c96d1af40594885352: "{{unknown}}"
  _oembed_c7d5899e7693e872c42d5f1447d49602: "{{unknown}}"
  _oembed_f42248010fde74fb9ccf25b8c0fd99ef: "{{unknown}}"
author:
  login: andrewjw
  email: andrewjwilkinson@gmail.com
  display_name: Andrew Wilkinson
  first_name: Andrew
  last_name: Wilkinson
permalink: "/2011/01/14/rsync-backups-to-amazon-s3/"
---
Having recently got married I wanted to make sure all the photos taken at the event are safely stored for the posterity. I thought I'd take the opportunity of making sure that all the rest of my photos are safely backed up, and that any new ones are also backed up without me needing to do anything.n
One of the simplest places to keep your backups is <a href="http://aws.amazon.com/s3/">Amazon S3</a>. There is essentially an unlimited amount of space available, and it's pretty cheap. <a href="http://samba.anu.edu.au/rsync/"><tt>rsync</tt></a> is a great tool to use when backing up because it only copies files, and parts of files that have changed so it will reduce the amount of data transferred to the lowest amount of possible. With S3 you not only pay for the data stored, but also for the data transferred so <tt>rsync</tt> is perfect. So, how do we use rsync to transfer data to S3?n
I won't go through setting up an Amazon S3 or creating a bucket, the <a href="http://docs.amazonwebservices.com/AmazonS3/latest/gsg/">Amazon documentation</a> does that just fine.n
The first thing to do is <a href="http://code.google.com/p/s3fs/wiki/InstallationNotes">download and install</a> <a href="http://code.google.com/p/s3fs/">s3fs</a>. This is a tool that uses <a href="http://fuse.sourceforge.net/">FUSE</a> to mount your S3 account as if it was an ordinary part of your filesystem. Once you've got it installed you need to configure it with your access and secret ids. You'll be given these when you set up your S3 account. Create a file <tt>.passwd-s3fs</tt> in your home directory and <tt>chmod</tt> it so it has no group or other permissions.n
Mounting your S3 bucket is simple, just run:<br />
[code]<br />
s3fs bucket_name /mount/point<br />
[/code]n
Any file operations you conduct in <tt>/mount/point</tt> will now be mirrored to S3 automatically. Neat!n
To copy the files across we need to run <tt>rsync</tt>.n
[code]<br />
rsync -av --delete /backup/directory /mount/point<br />
[/code]n
This will copy all files from <tt>/backup/directory</tt> to <tt>/mount/point</tt> and so to S3. The <tt>-a</tt> option means archive mode, which sets the correct options for performing a backup. <tt>-v</tt> is verbose so you can see how far it gets while <tt>--delete</tt> means that files will be deleted from <tt>/mount/point</tt> if they've been deleted from the directory your backing up.n
On your initial backup you'll likely be transferring multiple gigabytes of data, and that will saturate the upload on your Internet connection. This prevents you from doing pretty much anything else until it's finished, so lets look at limiting how fast the back up runs.n
<a href="http://monkey.org/~marius/pages/?page=trickle">trickle</a> is a very useful program that limits the bandwidth that a single program can consume. We don't want to limit <tt>rsync</tt>, because that is running locally, it's the <tt>s3fs</tt> program we want to limit so alter the mount command to be:n
[code]<br />
trickle -u 256 s3fs bucket_name /mount/point<br />
[/code]n
This will only allow s3fs to consume a maximum of 256KB/s of upload, allowing you to continue to browse Facebook while the backup is progressing. Simply change to the upload number depending on how fast your internet connection to get the right balance between a usable connection and the speed of the backup.n
To automate the backup just add the two commands to a script file and put it in your crontab like so.n
[code]<br />
@daily /home/username/bin/s3_backup<br />
[/code]n
