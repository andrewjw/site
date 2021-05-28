---
layout: post
title: Replacing Travis CI With BuildBot
date: 2021-05-28
tags:
- travis
- buildbot
- blog
- open source
permalink: "/2021/05/28/replacing-travis-ci-with-buildot/"
flickr_user: 'https://www.flickr.com/photos/99781513@N04/'
flickr_username: Scott Lewis
flickr_image: 'https://live.staticflickr.com/7577/16086839412_099ea08f05.jpg'
flickr_imagelink: 'https://www.flickr.com/photos/99781513@N04/16086839412/'
flickr_imagename: 'Brick laying'
---
Back when I reactivated this blog I [posted about using Travis CI](/2020/09/30/is-this-thing-on/) to
automate the build process. Sadly at the end of last year Travis
[announced](https://blog.travis-ci.com/2020-11-02-travis-ci-new-billing) they were ending free builds
for all public repositories, and only authorised open source projects will now get free build credits.

The [repository](https://github.com/andrewjw/site) for this blog is publically accessible, partly in case
anyone wants to see my draft posts, or raise a merge request to fix a typo, but mostly because why not?
That previously allowed me to not worry about the cost of building the site, but it's not unreasonable
for a private company who need to make a profit to want to focus their generosity on actual open-source
projects. I certainly don't blame them for the policy change, although I hope the approval process for
open source projects is easy and widely applied, so it's not just a few big projects that can take
advantage of it.
<!--more-->

There are many other build services out there, but I don't really want to pay to build my blog,
so I focused on finding an easy to use open-source CI system I could run locally. In the end, I settled
on [BuildBot](http://buildbot.net/) which has been around since the early 2000s, and I actually have
some experience with it from around that time. BuildBot has the advantage of being Python-based (one of
my preferred languages) and it uses Python as its configuration language so setting it up should be
straightforward.

I already have a [number of Docker containers](/2020/10/14/house-measurements/) running on my Synology
NAS. Adding Buildbot requires adding two more, a `buildmaster` and a `worker`. The build master needs
no special handling, you can run the standard Docker image and just mount a configuration file into the
right location. For the worker, it needs a little more thought as you need to bake any dependencies into
your image so they're available to the builds. It is relatively straightforward to build on top of the
default worker image, and my `Dockerfile` can be found
[here](https://github.com/andrewjw/docker/blob/master/worker/Dockerfile).

One problem I encountered was that the Buildbot documentation is focused on the model of one project
that has one BuildBot instance, but I need to share the builder across multiple projects. Fortunately, it
works well if you have a `SingleBranchScheduler` per project, and use a `ChangeFilter` to filter the
incoming webhooks from GitHub.

```python
c['schedulers'].append(schedulers.SingleBranchScheduler(
                            name="all",
                            change_filter=util.ChangeFilter(
                                        project='andrewjw/site'),
                            treeStableTimer=None,
                            builderNames=["site"]))
```

Each scheduler points to a different builder, which uses a unique `BuildFactory` to specify the build steps.
I try and keep my configuration in a `buildbot.sh` within the projects themselves.

```python
factory = util.BuildFactory()
env={"GEM_HOME":"/home/buildbot/.gem/ruby/2.7.0"}
factory.addStep(
    steps.Git(
        repourl='git@github.com:andrewjw/site',
        mode='incremental'))
factory.addStep(
    steps.ShellCommand(
        command=["bash", "./buildbot.sh"],
        env=env))
```

One advantage of Travis was that much of the build process was automated, and you didn't need to configure it.
With BuildBot you need to specify every step, and the running of code only on master, or only on a tag is not as
simple. After much trial and error, the following code works. You can see the full file in the
[glowprom project](https://github.com/andrewjw/glowprom/blob/master/buildbot.sh). First, we extract the branch
name of the current checkout, then compare it to `master` or use a prefix match to determine if we're on a tagged
version. When running on `master` the Semantic release call is the final step, so we know all the tests have
passed. This will tag a release, which again triggers the pipeline, but this is a tag with a `v` as the
initial character, so we build a Docker image and push it to the Docker Hub.

```bash
BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "Building branch $BRANCH"
if [[ "$BRANCH" == "master" ]]; then
  COVERALLS_REPO_TOKEN=$GLOWPROM_COVERALLS_REPO_TOKEN coveralls
  semantic-release publish
fi
if [[ ${BRANCH:0:7} == "heads/v" ]]; then
    ./docker_push.sh
fi
```

Timeliness of feedback on your commit is an important factor in enabling quick developer cycle times. Travis
enabled that by using a webhook so it was notified immediately when you pushed a commit. The problem with running
BuildBot internally is that it isn't externally accessible. BuildBot makes it easy to run a scheduled build, so you
can build every day, hour or even more frequently if you want. The problem is that you have to wait for that build
to be triggered to get feedback on your commit, or you could manually trigger it, but who wants to add a manual step
like that?

Fortunately, I already host this blog on Linode, and I have a VPN set up between the server and my internal network.
I added the below config to the Apache instance that serves the blog. For my external DNS name it uses `mod_proxy`
to forward requests to `/change_hook/github` on to the BuildBot instance, which will go via the VPN. GitHub and
BuildBot already supports a shared secret for authentication that the request is valid. This is set up when you
add the webhook to the GitHub API.

```xml
<VirtualHost *:80>
    ServerName external.dns.name

    <Location /change_hook/github>
        ProxyPass http://internal.dns.name:8010/change_hook/github
        ProxyPassReverse http://internal.dns.name:8010/change_hook/github
        <Limit POST>
            Order allow,deny
            Allow from all
        </Limit>
    </Location>
</VirtualHost>
```

Requiring a remote server and VPN adds a significant amount of complexity to the setup. I believe most home routers support
some form of port forwarding, so you could probably also use that. However, I would be concerned about exposing more of my home network
to the internet than necessary. Please let me know in the comments if you have any suggestions on how to simplify the setup.

This setup has been running for a couple of months and seems to be working well. It is both reliable and means I can sleep easy,
knowing I'm not leeching of a company who were just trying to help real open source projects.
