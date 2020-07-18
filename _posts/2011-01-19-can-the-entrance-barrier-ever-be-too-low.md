---
layout: post
title: Can the entrance barrier ever be too low?
date: 2011-01-19 13:36:50.000000000 +00:00
type: post
parent_id: '0'
published: true
password: ''
status: publish
categories:
- etiquette of programming
tags:
- code
- google
- google code
- open source
- programming
meta:
  _edit_last: '364050'
  _wpas_done_twitter: '1'
author:
  login: andrewjw
  email: andrewjwilkinson@gmail.com
  display_name: Andrew Wilkinson
  first_name: Andrew
  last_name: Wilkinson
permalink: "/2011/01/19/can-the-entrance-barrier-ever-be-too-low/"
---
<a href="http://www.flickr.com/photos/thecrazyfilmgirl/3248283617/"><img src="{{ site.baseurl }}/assets/3248283617_c23445ea31_m.jpg" alt="Stop Sign by thecrazyfilmgirl" style="float:right;border:0;" /></a>Yesterday Google <a href="http://googlecode.blogspot.com/2011/01/make-quick-fixes-quicker-on-google.html">announced</a> a new feature for <a href="http://code.google.com/p">Google Code's Project Hosting</a>. You can now edit files directly in your browser and commit them straight into the repository, or, if you don't have commit privileges, attach your changes as a patch in the issue tracker.n
If you're trying to run a successful open source project then the key thing you want is more contributors. The more people adding to your project the better and more useful it will become, and the more likely it is to rise out of the swamp of forgotten, unused projects to become something that is well known and respected.n
It's often been said that to encourage interaction you need to lower the barrier so that people can contribute with little or no effort on their part. Initially open source projects are run by people who are scratching their own itches, and producing something that is useful to themselves. Google's intention with this feature is clearly to allow someone to think "Project X" has a bug, I'll just modified the code and send the developers a patch. The edit feature is very easy to find, with a prominent "Edit File" link at the top of the screen when you're browsing the source code so Google have clearly succeeded in that respect.n
[caption id="attachment_322" align="alignleft" width="400" caption="Editing a file on Google Code"]<a href="http://andrewwilkinson.files.wordpress.com/2011/01/googlecodeedit.png"><img src="{{ site.baseurl }}/assets/googlecodeedit.png" alt="" title="Google Code&#039;s Edit File Feature" width="400" height="333" class="size-full wp-image-322" /></a>[/caption]n
My big concern here is that committing untested code to your repository is right up there at top of the list of things that programmers should never, ever, do. I like to think of myself as an expert Python programmer, but I'll occasionally make simple mistakes like missing a comma or a bracket. It's rare that anything beyond a trivially small change will work perfectly first time. Only by running the code do you pick up these and ensure that your code is at least partially working.n
I'm all for making it easy to contribute, but does contributing a large number of untested changes really help anyone? I'm not so sure. Certainly this feature is brilliant for making changes to documentation where all you need to do is to read the file to know that the change is correct, but it seems a long way from best-practice for making code changes.n
Perhaps I should be thinking about this as a useful tool for sketching out possible changes to code. If you treat it as the ability to make 'pseudo-code' changes to a file to demonstrate how you might tackle a problem it seems to make more sense, but open source has always lived by the mantra 'if you want it fixed, fix it yourself'.n
I suppose I should worry about getting my <a href="http://code.google.com/p/djangode/">pet open source project</a> to a state where people want to contribute changes of any quality, and then I can worry about making the changes better!n
<hr />
Photo of <a href="http://www.flickr.com/photos/thecrazyfilmgirl/3248283617/">Stop Sign</a> by <a href="http://www.flickr.com/photos/thecrazyfilmgirl">thecrazyfilmgirl</a>.n