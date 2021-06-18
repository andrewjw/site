---
layout: post
title: The Power Of Team Dashboards
date: 2021-06-18
tags:
- dashboards
- management
permalink: "/2021/06/18/power-of-team-dashboards/"
flickr_user: 'https://www.flickr.com/photos/smemon/'
flickr_username: Sean MacEntee
flickr_image: 'https://live.staticflickr.com/3914/14618772953_45f8cbf809.jpg'
flickr_imagelink: 'https://www.flickr.com/photos/smemon/14618772953/'
flickr_imagename: 'measuring tape'
---
Using metrics and dashboards is a well-understood tool when monitoring the health and performance
of software, or your profitability or other key business metrics. What is less common is using
the same tools and techniques to monitor the health and performance of the team behind the
software. I'm not suggesting using dashboards to report on individual developers, but as a tool
to help the team focus on improving their own processes, it can be very useful, provide it's
handled carefully.

My own journey started when I was promoted from a team leader to an engineering manager, responsible
for five teams. The change in level resulted in a significantly different view, but also great
difficulty in knowing where to focus my efforts. When you're a team leader you are so close to
the team that you hear and feel every change in mood, and have intimate knowledge of all projects
and their current state. Suddenly being responsible for five teams gives you a great view to take
advantage of areas of collaboration between teams, and removes you from the noise of day to day
life so you can focus on the biggest issues. However, it also removes you from the firehose of
raw information so it can be hard to know where you should spend your time to get the best return
on your energy.
<!--more-->

The solution to this problem is the same as it would be for a software system you want to improve,
measure everything! Error rates, latency, memory usage, throughput - measuring software has a
long history, but measuring a team is much tricker. Firstly decide how to measure, and then what
to measure. Start small, and gradually add metrics as you find areas that would be useful to
report on.

How to measure is simple, just use whatever technology your company standardises on for dashboards.
In my case, I started with a Python script that wrote to a Google Sheet and displayed the data in
a Google Data Studio Report. As the report evolved we transitioned to using some company standard
and some custom BigQuery databases. Whatever technology you use make sure it's automated, that it
runs regularly and that it produces something that is easily and widely available.

When deciding what to measure start with any team, department or company goals you might have
about team performance. In Ocado's case, there is a company level goal around
[PeakOn scores](https://peakon.com/) so we used a BigQuery dataset to visualise our results. Next,
consider what factors you think will affect team morale the most. This might be the number of on-call
escalations, the [MTTR](https://en.wikipedia.org/wiki/Mean_time_to_repair) for incidents, or
something else. Lastly, you could look at leading indicators for the team delivery performance.

Tracking metrics that are lagging indicators of performance is common - number of tickets completed,
the cycle time of completed tickets, etc. While there is some value in these, they don't help you in
deciding where to focus to help the team deliver. If you spot a dip in completed tickets then it's
too late, the dip has already occurred. You can then react and try to work out why it dipped, but
it's much better if you can prevent the dip in the first place. Some example leading indicators are:

- **Number of tickets in progress**. An increase here can indicate tickets not being completed, but
  new ones still being started.
- **Time spent in progress for current tickets**. Similar to cycle time, this metric should look at how
  long tickets that haven't been completed have been in progress. An increase in this will precede
  an increase in cycle time and might indicate that developers are struggling to complete or deploy their
  changes.
- **Tickets that have exceeded 90% of your cycle time**. Rather than a number, this should be a list of
  tickets that are already guaranteed to increase your cycle time.

Once you have a simple dashboard up and running you need to ensure the data is looked at and reacted to
regularly. To do this integrate the dashboard into your leadership team rituals so thinking about it
becomes second nature. I check the report every Monday morning and talk to my team leaders about
anything that jumps out at me. As a group, we also discuss the cycle time and on-call escalation charts
as any change in those could quickly derail our delivery plans. We also have a whole department get
together every other week where I talk through any trends and ask the developers to think about what
their team can do to improve things, or how I can help them.

When talking to a department of developers you clearly need to tailor your messaging differently to
when you are talking to a group of team leads. Focus on areas that are important to the morale of your
teams. This will likely be the feeling that they are able to work quickly (i.e. cycle time) and how
much time is spent dealing with support issues.

It's particularly important when talking to a room of developers to treat your dashboard as a guide,
and not a stick. Definitely do not use it to evaluate individual developers, and try to avoid the
temptation to compare teams against each other. Every team has its own set of challenges, and what's
important is that everyone is learning and getting better, not who is "winning". It's very useful
to have the ability to filter your dashboard to an individual team but avoid adding the ability
to include multiple teams at the same time.

Earlier I mentioned including a list of tickets that have exceeded 90% of your usual cycle time. This
will produce a list of tickets with issues and are therefore worthy of extra attention, but highlighting
them during team meetings can be dangerous. It's very easy for developers to treat a ticket being called
out for taking an unusually long time as an attack on them or their abilities. This should not be the
case, and it should be an opportunity for the team to discuss how they can improve to get this ticket
completed and to prevent similar tickets from stalling.

To allow teams to deal with long tickets you shouldn't call them out during larger meetings. Definitely
do not include assignee names on any dashboards, instead just include ticket numbers, titles and team
names. Team leaders should use the report to steer discussions towards problematic tickets during standups
or retrospectives.

I have found having a team dashboard an invaluable tool that has made me a better, more proactive manager.
If you start small, iterate, and embed your dashboards into your team rituals from the start you'll quickly
see how you can focus your energies where it can have the most impact.

Let me know what metrics you use, and how dashboards fit into your rituals in the comments below!
