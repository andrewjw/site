---
layout: post
title: Using Fabric For Deployment
date: 2010-06-16 13:18:02.000000000 +01:00
tags:
- deployment
- automatic deployment
- automation
- django
- fabric
- python
- script
- scripting
permalink: "/2010/06/16/using-fabric-for-deployment/"
flickr_user: 'http://www.flickr.com/photos/donsolo/'
flickr_username: "s o l o"
flickr_image: 'https://live.staticflickr.com/3187/2458233987_5f5951a48e_w.jpg'
flickr_imagelink: 'http://www.flickr.com/photos/donsolo/2458233987/'
flickr_imagename: robot invasion
---
In a [previous post](/2010/04/15/perfect-deployment-of-websites) I discussed what you want from an automatic
deployment system. In this post I'll discuss how use to solve the repeatability and scalability requirements
that I set out.

Fabric is a tool which lets you write scripts to automate repetitive tasks. So far, so bash like. What sets
[Fabric](http://fabfile.org) apart is the tools it gives you to run commands on remote servers. Fabric allows
you to run the same commands on multiple machines, and to move files between the hosts easily.

To get started with Fabric you'll need to install it, but a simple `sudo easy_install fabric` should be enough
to get you up and running. The Fabric website has excellent documentation, including a
[tutorial](http://docs.fabfile.org/0.9.1/tutorial.html), but before I discuss how to integrate Fabric with
your Django deployment process, lets go over the basics.

A Fabric control file is a Python file named `fabfile.py`. In it, you define a series functions, one for each
command that you want to run on the remote servers.

```python
from fabric.context_managers import cd
from fabric.operations import sudon
env.hosts = ['host1', 'host2']
def update():
    with cd('/data/site'):
        sudo('svn up')
        sudo('/etc/init.d/apache2 graceful')
```

 We've defined the function `update` which can be run by typing `fab update` in the same directory as
`fabfile.py`. When run, Fabric will connect in turn to `host1` and `host2` and run `svn up` in `/data/site`
and then restart Apache.

Typically I define two functions. An `update` command, like that above is used to update the site where is has
previously been deployed. A `deploy` command is used to checkout the site onto a new machine. Fabric lets you
override the host list on the command line using the `-H` option. To deploy one of my sites on a new box I
just have to type `fab -H new-machine deploy` and the box is set up for me.

Fabric helps you fulfil a few of the requirements for a perfect deployment system. It is scaleable, as to
extend your system to a new machine you only need to add the hostname to the `env.hosts` list. It is also
repeatable, providing you put every command you need to run to update your site into your `fabfile`.

With an automated deployment system in place we can now move on to looking a dependency, settings and database
change management, but those are subjects for a future post.
