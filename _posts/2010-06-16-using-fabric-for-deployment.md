---
layout: post
title: Using Fabric For Deployment
date: 2010-06-16 13:18:02.000000000 +01:00
type: post
parent_id: '0'
published: true
password: ''
status: publish
categories:
- deployment
tags:
- automatic deployment
- automation
- django
- fabric
- python
- script
- scripting
meta:
  _edit_last: '364050'
  _wp_old_slug: ''
  _wpas_done_twitter: '1'
  _oembed_27627370d34d7e9f479f39f5eb244219: "{{unknown}}"
  _oembed_14a69955b5d2a69e90d41eea6b33df5f: "{{unknown}}"
  _oembed_ff7ad970097524c4dfd2eec46efd28d1: "{{unknown}}"
  _oembed_314bf6955082ab2a39b4799d2da7ce2c: "{{unknown}}"
  _oembed_1fb46b316a871dd0aa00c4bce2d3368a: "{{unknown}}"
  _oembed_593fe04ee4a68c98343a72596ae21738: "{{unknown}}"
  _oembed_4643431b8f86034e87231898c4f9c37b: "{{unknown}}"
  _oembed_98d440e1c59a1dd60136865f8220cd2f: "{{unknown}}"
  _oembed_4b8efb124e939bb0c1934c9763cb7039: "{{unknown}}"
  _oembed_63d0fa9091bfc53c2240f24b78d8d192: "{{unknown}}"
author:
  login: andrewjw
  email: andrewjwilkinson@gmail.com
  display_name: Andrew Wilkinson
  first_name: Andrew
  last_name: Wilkinson
permalink: "/2010/06/16/using-fabric-for-deployment/"
---
<img src="{{ site.baseurl }}/assets/2458233987_5f5951a48e_m.jpg" alt="robot invasion by donsolo" style="float:right;" />In a <a href="http://andrewwilkinson.wordpress.com/2010/04/15/perfect-deployment-of-websites">previous post</a> I discussed what you want from an automatic deployment system. In this post I'll discuss how use to solve the repeatability and scalability requirements that I set out.n
Fabric is a tool which lets you write scripts to automate repetitive tasks. So far, so bash like. What sets <a href="http://fabfile.org">Fabric</a> apart is the tools it gives you to run commands on remote servers. Fabric allows you to run the same commands on multiple machines, and to move files between the hosts easily.n
To get started with Fabric you'll need to install it, but a simple <tt>sudo easy_install fabric</tt> should be enough to get you up and running. The Fabric website has excellent documentation, including a <a href="http://docs.fabfile.org/0.9.1/tutorial.html">tutorial</a>, but before I discuss how to integrate Fabric with your Django deployment process, lets go over the basics.n
A Fabric control file is a Python file named <tt>fabfile.py</tt>. In it, you define a series functions, one for each command that you want to run on the remote servers.n
[sourcecode language="python"]<br />
from fabric.context_managers import cd<br />
from fabric.operations import sudon
env.hosts = ['host1', 'host2']n
def update():<br />
    with cd('/data/site'):<br />
        sudo('svn up')<br />
        sudo('/etc/init.d/apache2 graceful')<br />
[/sourcecode]n
We've defined the function <tt>update</tt> which can be run by typing <tt>fab update</tt> in the same directory as <tt>fabfile.py</tt>. When run, Fabric will connect in turn to <tt>host1</tt> and <tt>host2</tt> and run <tt>svn up</tt> in <tt>/data/site</tt> and then restart Apache.n
Typically I define two functions. An <tt>update</tt> command, like that above is used to update the site where is has previously been deployed. A <tt>deploy</tt> command is used to checkout the site onto a new machine. Fabric lets you override the host list on the command line using the <tt>-H</tt> option. To deploy one of my sites on a new box I just have to type <tt>fab -H new-machine deploy</tt> and the box is set up for me.n
Fabric helps you fulfil a few of the requirements for a perfect deployment system. It is scaleable, as to extend your system to a new machine you only need to add the hostname to the <tt>env.hosts</tt> list. It is also repeatable, providing you put every command you need to run to update your site into your <tt>fabfile</tt>.n
With an automated deployment system in place we can now move on to looking a dependency, settings and database change management, but those are subjects for a future post.n
<hr />
Photo of <a href="http://www.flickr.com/photos/donsolo/2458233987/">robot invasion</a> by <a href="http://www.flickr.com/photos/donsolo/">donsolo</a>.n
