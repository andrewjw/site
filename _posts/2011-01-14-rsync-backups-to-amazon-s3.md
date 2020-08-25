---
layout: post
title: Rsync backups to Amazon S3
date: 2011-01-14 12:00:00.000000000 +01:00
tags:
  - amazon
  - backup
  - linux
  - rsync
  - s3
  - trickle
  - unix
permalink: /2011/01/14/rsync-backups-to-amazon-s3/
---
Having recently got married I wanted to make sure all the photos taken at the event are safely stored for the
posterity. I thought I'd take the opportunity of making sure that all the rest of my photos are safely backed
up, and that any new ones are also backed up without me needing to do anything.

One of the simplest places to keep your backups is [Amazon S3](http://aws.amazon.com/s3/). There is
essentially an unlimited amount of space available, and it's pretty cheap.
[`rsync`](http://samba.anu.edu.au/rsync/) is a great tool to use when backing up because it only copies files,
and parts of files that have changed so it will reduce the amount of data transferred to the lowest amount of
possible. With S3 you not only pay for the data stored, but also for the data transferred so `rsync` is
perfect. So, how do we use rsync to transfer data to S3?

I won't go through setting up an Amazon S3 or creating a bucket, the [Amazon
documentation](http://docs.amazonwebservices.com/AmazonS3/latest/gsg/) does that just fine.

The first thing to do is [download and install](http://code.google.com/p/s3fs/wiki/InstallationNotes)
[s3fs](http://code.google.com/p/s3fs/). This is a tool that uses [FUSE](http://fuse.sourceforge.net/) to mount
your S3 account as if it was an ordinary part of your filesystem. Once you've got it installed you need to
configure it with your access and secret ids. You'll be given these when you set up your S3 account. Create a
file `.passwd-s3fs` in your home directory and `chmod` it so it has no group or other permissions.n Mounting
your S3 bucket is simple, just run:

```bash
s3fs bucket_name /mount/point
```

Any file operations you conduct in `/mount/point` will now be mirrored to S3 automatically. Neat!

To copy the files across we need to run `rsync`.

```bash
rsync -av --delete /backup/directory /mount/point
```

This will copy all files from `/backup/directory` to `/mount/point` and so to S3. The `-a` option means
archive mode, which sets the correct options for performing a backup. `-v` is verbose so you can see how far
it gets while `--delete` means that files will be deleted from `/mount/point` if they've been deleted from the
directory your backing up.

On your initial backup you'll likely be transferring multiple gigabytes of data, and that will saturate the
upload on your Internet connection. This prevents you from doing pretty much anything else until it's
finished, so lets look at limiting how fast the back up runs.

[trickle](http://monkey.org/~marius/pages/?page=trickle) is a very useful program that limits the bandwidth
that a single program can consume. We don't want to limit `rsync`, because that is running locally, it's the
`s3fs` program we want to limit so alter the mount command to be:

```bash
trickle -u 256 s3fs bucket_name /mount/point
```

 This will only allow s3fs to consume a maximum of 256KB/s of upload, allowing you to continue to browse
Facebook while the backup is progressing. Simply change to the upload number depending on how fast your
internet connection to get the right balance between a usable connection and the speed of the backup.

To automate the backup just add the two commands to a script file and put it in your crontab like so.

```crontab
@daily /home/username/bin/s3_backup
```
