---
layout: post
title: Sustainable Software Development
date: 2023-11-16
tags: management
permalink: "/2023/11/09/sustainable-software/"
---
When you're in the zone it can be hard to think about the future of the code you're writing, but
the time you're spending writing it is just a fraction of its overall lifespan. Code may be written
once, but it will be edited a few times, perhaps copied once or twice, and likely executed many
hundred, if not thousands or millions of times. You as a software developer will (hopefully) have
a long and productive time in software development, as will the team you work with. And finally, you
also do your work on planet Earth (hi to any readers on the
[ISS](https://en.wikipedia.org/wiki/International_Space_Station)), and without it you'd really
struggle.

When creating or modifying an object or system that we intend to last for a long time, it is crucial
to take sustainability into account. This includes factors such as the sustainability of the source
code, your or your team's ability to work on it for an extended period of time, and the impact that
the software will have on the environment. All of these aspects are significant and should be
carefully considered.

If you're working in a scrappy start-up, fighting for survival, then the long term maintainability
of your code will not be important to you. In the majority of cases though, code can be expected to last
for a significant period of time, and the cost of maintaining will begin to outweigh the initial
cost of writing it.

Code that is not maintained will accumulate problems. Libraries it relies on will have new releases,
as will operating systems it runs on. This will provide new features, fix bugs and solve security
vulnerabilities. Software that has not been touched for a while requires signifantly more time to make
simple changes, compared to software that is regularly touched.

The DevOps movement helps significantly with maintainability as any manual process is something that ages
very quickly. Even with excellent documentation it's difficult to reliably follow a process you're not
familiar with. Automation, particularly the build, test and deployment are well worth the time spent on
building them. If you can combine a tool like (Renovate)[https://github.com/renovatebot/renovate] with
a high quality test suite, and a continous deployment pipeline, you can focus on other things, safe in
the knowledge that your application is being kept up to date with the latest security fixes.

Beyond automation, how you write code will affect how sustainable and how easy maintain your code base is.
This doesn't mean you should add comments everywhere, indeed if you need comments then your code could
probably be clearer. Not that there aren't times when comments to explain why a section of code is written
as it is are needed, but they should be rare.

When writing your code, think about how it will be read, and how it will be maintained. This starts with the
language you use, as well as the libraries and frameworks and the design patterns you choose. Clearly there's
no language, library or framework that's perfect for all situations, but there's are bad choices. The two things
to consider when making a choice are how much knowledge of the technology is there in your company (or are much
time will you invest in training), and what is the community of the project like.

While you might think Kotlin (to pick a random example) is the perfect choice for your new application, if no
other apps in your company in use Kotlin, and knowledge amongst your colleagues is low then it will be hard
to maintain in the future. Similarly with frameworks and libraries, the ability for other developers to jump
between applications and focus on the logic and not the surrounding implementing details can hardly be over
estimated. Languages and libraries don't by themselves deliver value. They might enable you to deliver value
quicker compared to other choices, but only if you can unlock that advantage, and maintain it long term.

The other aspect is the community around the technology, and where you are comfortable sitting on the 
[technology adoption lifecycle](https://en.wikipedia.org/wiki/Technology_adoption_life_cycle). It's certainly
a good idea to keep abreast of new developments, and experiment with them by building things you're happy
to throw away once you've learned about them. Betting your company of a brand new library, that's only existed
for a month and has one contributor, has a high risk of you depending on code that's been abandoned and either
needing to migrate away from it, or commit to supporting it yourself. At the other end of the lifecycle, if you
wait too long to adopt, or stay with a dependency for too long, then it may move out of support and be abandoned
too - exposing you to unpatched security vulnerabilities, and conflicts when other dependencies drop support for
something you are using.
