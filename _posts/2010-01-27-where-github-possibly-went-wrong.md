---
layout: post
title: Where GitHub (Possibly) Went Wrong
date: 2010-01-27 13:21:33.000000000 +00:00
type: post
tags:
- git
- github
- programming
- stack overflow
- version control
- other websites
permalink: "/2010/01/27/where-github-possibly-went-wrong/"
flickr_user: 'https://www.flickr.com/photos/bitzcelt/'
flickr_username: Mike Bitzenhofer
flickr_image: 'https://live.staticflickr.com/2022/2248163114_73723d627f_w.jpg'
flickr_imagelink: 'https://www.flickr.com/photos/bitzcelt/2248163114/'
flickr_imagename: 8 Forks
---
While on my delayed train this morning I was listening to <a href="http://blog.stackoverflow.com/2010/01/podcast-80/">episode 80</a> of the excellent <a href="http://blog.stackoverflow.com/">Stack Overflow podcast</a>. In this episode Jeff Atwood was complaining to Joel Spolsky about his problems with <a href="http://www.github.com">GitHub</a>.

GitHub is a social coding site, along the same lines as Sourceforge or Google Code, but focused entirely on the distributed version control system Git. Where GitHub differs from the other project hosting sites, and where I think Jeff's confusion comes from is that with GitHub the primary structure on their site is that of the developer, not of the project. They treat every developer as a rock star, who is bigger than the projects that they work on.

GitHub makes it incredibly easy to take a codebase, make your own changes and to publish them to world. What GitHub fails to do is to encourage people to collaborate together to push one code base forward. What I'm not suggestion is that branching is a bad idea. Branching code is a useful coding technique which can be used to separate in-development features from other changes until the code has stabilised again. What GitHub focuses on is the changes that an individual developer makes, not the changes required for a particular feature.

<div style="float: left; margin-right: 5px;">
<a data-flickr-embed="true" href="https://www.flickr.com/photos/calliope/322623000/" title="dewy branch"><img src="https://live.staticflickr.com/128/322623000_73f45dc589_w.jpg" width="400" height="267" alt="dewy branch"></a><script async src="//embedr.flickr.com/assets/client-code.js" charset="utf-8"></script>
</div>

When a developer creates a copy of some code of GitHub they get a wiki and an issue tracker as well. This further confuses matters because not only do you have trouble knowing which git tree is the correct one to pull from, but you also don't know where to report bugs or go to for documentation.

Google Code seems to be in a better position for combining distributed version control with project management. They have an excellent wiki and issue tracker, and give each project a straightforward and simple homepage. You can also use Mercurial, which is similar to git, as your version control system. All that they need to do is allow developers to publish their own changes, but in a markedly separate section to the core code of the project.

I can see how GitHub is nice for developers, but in any mildly successful open source project the number of users vastly outweighs the number of developers. It seems crazy to me to make your primary web presence suited only for the minority of people who are involved with the project.
