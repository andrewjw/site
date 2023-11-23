---
layout: post
title: Sustainable Software Development
date: 2023-11-16
tags: management
permalink: "/2023/11/09/sustainable-software/"
unsplash_image: mouse_ivy.jpg
unsplash_title: White Apple Magic Mouse Beside Green Leaves
unsplash_url: https://unsplash.com/photos/white-apple-magic-mouse-beside-green-leaves-a3pA4QNHVbk
unsplash_user: "@larisabirta"
---
When you're in the zone it can be hard to think about the future of the code you're writing, but
the time you're spending writing it is just a fraction of its lifespan. Code may be written
once, but it will be edited a few times, perhaps copied once or twice, and likely executed many
hundred, if not thousands or millions of times. You as a software developer will (hopefully) have
a long and productive time in software development, as will the team you work with. And finally, you
also do your work on planet Earth (hi to any readers on the
[ISS](https://en.wikipedia.org/wiki/International_Space_Station)), and without it you'd really
struggle.

When creating or modifying an object or system that we intend to last for a long time, it is crucial
to consider sustainability. This includes factors such as the sustainability of the source
code, your or your team's ability to work on it for an extended period, and the software's impact on
the environment. All of these aspects are significant and should be
carefully considered.

If you're working in a scrappy start-up, fighting for survival, then the long-term maintainability
of your code will not be important to you. In most cases though, code can be expected to last
for a significant time, and the cost of maintaining it will significantly outweigh the initial
cost of writing it.
<!--more-->

Code that is not maintained will accumulate problems. Libraries it relies on will have new releases,
as will the operating system it runs on. These will provide new features, fix bugs and solve security
vulnerabilities. Software that has not been touched for a while requires significantly more time to make
simple changes, compared to software which is regularly altered.

The DevOps movement helps significantly with maintainability as any manual process ages
very quickly. Even with excellent documentation, it isn't easy to reliably follow a process you're not
familiar with. Automation, particularly the build, test and deployment steps, are well worth the time spent on
building them. If you can combine a tool like [Renovate](https://github.com/renovatebot/renovate) with
a high-quality test suite, and a continuous deployment pipeline, you can focus on other things, safe in
the knowledge that your application is being kept up to date with the latest security fixes.

Beyond automation, how you write code will affect how sustainable and easy to maintain your code base is.
This doesn't mean you should add comments everywhere, indeed if you need comments then your code could
probably be clearer. Not that there aren't times when comments to explain why a section of code is written
as it is are needed, but they should be rare.

When writing your code, think about how it will be read, and how it will be maintained. This starts with the
language you use, as well as the libraries, frameworks and design patterns you choose. No language, library
or framework is perfect for all situations, but there are bad choices. The two things
to consider when making a choice are how much knowledge of the technology there is in your company (or how much
time you are willing to invest in training), and what the community of the project is like.

While you might think Kotlin (to pick a random example) is the perfect choice for your new application, if no
other apps in your company use Kotlin, and knowledge amongst your colleagues is low then it will be hard
to maintain in the future. Similarly, with frameworks and libraries, the ability for other developers to jump
between applications and focus on the logic and not the surrounding implementing details can hardly be overestimated.
Languages and libraries don't by themselves deliver value. They might enable you to deliver value
quicker compared to other choices, but only if you can unlock that advantage, and maintain it long-term.

The other aspect is the community around the technology, and where you are comfortable sitting on the 
[technology adoption lifecycle](https://en.wikipedia.org/wiki/Technology_adoption_life_cycle). It's certainly
a good idea to keep abreast of new developments and experiment with them by building things you're happy
to throw away once you've learned about them. But betting your company on a brand new library, that's only existed
for a month and has one contributor, has a high risk of you depending on code that's been abandoned and either
needing to migrate away from it, or commit to supporting it yourself. At the other end of the lifecycle, if you
wait too long to adopt, or stay with a dependency for too long, then it may move out of support and be abandoned
too - exposing you to unpatched security vulnerabilities, and conflicts when other dependencies drop support for
something you are using.

Most software development projects last many months or years. For people working in an Agile fashion, there might not
even be a specific end goal, just an endlessly evolving set of requirements and software that is growing to meet them.
[Burnout is a significant issue in software development](https://www.forbes.com/sites/forbestechcouncil/2022/07/13/the-key-to-retaining-software-developers-stopping-burnout/)
and as a leader, it is your job to recognise the signs and work to prevent it. If your team burns out, productivity
and quality will collapse, and the costs will be much greater than if you had worked more sustainably.

Common reasons for burnout are poor working conditions, pressure and unrealistic deadlines, and a culture that
doesn't prioritise learning, improvement or balance in the demands on team members. This is a huge topic, far too
big for one blog post, but sacrificing a bit of speed now will result in happier developers and a much more sustainable
development process.

One of the most demoralising things about being a developer is working on software that is hard to change, but
you don't have the permission, or time, to make the needed improvements. By dedicating an appropriate amount
of time to [tech debt reduction](https://www.theandrewwilkinson.com/2022/02/03/dont-call-it-tech-debt/) you not
only end up with more sustainable software but a more sustainable culture of development too. As a leader,
you might need to defend this time, but by looking at security vulnerabilities in dependencies, or the risk that
you will no longer be able to get support should you need it, it is possible to build a strong business case
for this work.

The most common thing your code will do is run. Whether it's executing a thousand times a second, or once a week
when someone runs a report, it'll spend more time running than you spent writing it. Computers use energy, need
materials to build, and cost your company money to run. If you can halve the time it takes a process to run you'll
give your customers a better experience, save your company money, and reduce the impact your code has on the planet.

A centralised database clearly has a significantly smaller environmental impact than a blockchain-based ledger - even
if you take into account techniques like
[Ethereum's Proof of Stake](https://ethereum.org/en/developers/docs/consensus-mechanisms/pos/). Which one is better
depends on what your priorities are, and what tradeoffs you are willing to make. They are tradeoffs though, and they
demand consideration during your design process.

Not all tradeoffs are quite as extreme as the database vs blockchain example. You might be working on a report which
does some algorithmic processing of data. If you're writing in Python it'll likely take longer to run than if you
replace that section with highly optimised C code. Again, there are no right answers, but the Python code will likely
be significantly easier for your team to maintain in the future, so perhaps that is worth the extra costs incurred by
the longer run time.

It's easy to focus on the joy of building a complex system, one that will be useful to your customers and make money
for your company. But an often overlooked customer is you in the future, or those who come after you and have to look
after the system you are now building. When you are choosing the technology you will use and the systems architecture
you'll implement, make sure you consider how easy it will be to maintain, how your team will work without the risk of
burnout, and the impact your design choices will have on the planet.

Have you chosen one technology over another because of the ease of maintainability? Have you changed architecture because
of environmental concerns? Let me know in the comments below.
