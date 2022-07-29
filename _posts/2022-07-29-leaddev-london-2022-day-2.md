---
layout: post
title: LeadDev London 2022 Day 2
date: 2022-07-29
tags: conference leaddev
permalink: "/2022/07/29/leadev-london-2022-day-2/"
image: leaddev2022_welcome.jpeg
image_title: Welcome To LeadDev London 2022
---
Recently I was lucky enough to go to LeadDev London. You can read about my general thoughts, and the first
day of talks, [here](https://www.theandrewwilkinson.com/2022/06/17/leadev-london-2022-day-1/). This
post covers the second day.

The following is a summary of my notes from each talk. Any mistakes, errors or things that don't
make sense are entirely my fault. Hopefully, this will provide a flavour of each talk and inspire
you to watch the ones that interest you the most to get the full story.
<!-- more -->

## Why we are writing a monolith, not a microservice

_[Supriya Srivatsa](https://supriyasrivatsa.com/)_

This talk was particularly relevant to me as we have a lot of monolith applications, and we constantly talk
about the best way to split them into microservices... but maybe we don't need to?

A key part of good architecture is abstraction, but it doesn't need to be over a network.

At Atlassian they are building a _modular monolith_. Boundaries are hard to define, but you can use
domain driven modules to split the code base.

## A Commune in the Ivory Tower? - A new approach to architecture decisions

_[Andrew Harmel-Law](https://twitter.com/al94781)_

The typical way of making architectural decisions is that a team requests a decision. The architects
go and have a think, then the decision is received by the team, and they try to implement it. The
problem is that this doesn't scale and can significantly delay the team.

In this talk, Andrew Harmel-Law proposes a decentralised way of making decisions - The Advice Process.

Anyone can make a decision, but before doing so they must seek advice. There are two parts to this
process - a lightweight ADR (architectural decision record) and the Architecture Advice Forum.

The ADR is a document that describes a decision that was made (or is in the process of being made).
It should contain:

* The title
* Context - you should put real effort in so people can understand why you're making this decision.
* Consequences of the decision
* Advice - who gave what and when.

The Architecture Advice Forum is a weekly meeting to discuss in-progress ADRs and for people to give
and receive advice.

### How To Fail

1. "Bad" decisions - how do people deal with decisions they disagree with? Give advice, but let the team do what they want.
1. Old guard is the new guard - if you don't get new people writing ADRs
1. Off-the-grid decisions

The last of these is quite serious as people are not following the process. You should ask them to
write an ADR and find out why they didn't in the first place. Did they not realise it was a decision?

## Sorry... you go ahead. The art of making space and claiming space in meetings

_[Jemma Bolland](https://twitter.com/jemolova)_

Only 35% of people say they can contribute in meetings when they have a contribution to make.

Some people think to talk and others talk to think. Don't let your meeting be dominated by the latter
category of people.

Make sure everyone knows how you would like them to contribute, and before you attend a meeting, if you're
not confident, find out what areas you can best contribute to.

Leave space before moving on to the next point - ask "is there anything I haven't considered?"

## Using incidents to level up your teams

_[Lisa Karlin Curtis](https://twitter.com/paprikati_eng)_

Incidents...

* broaden your horizons.
* teach you to fail gracefully.
* teach you to make systems easier to debug.
* are a chance to spend time with, and learn from, the best.

To help people learn make incidents more accessible. You can lower the bar so you declare an
incident more frequently. This will help you to practice for the big incidents when they do
come.

Encourage everyone to participate by announcing incidents and sharing a public slack channel.

While resolving the incident show your working - share as much as you can, including what you
tried that didn't work so people can follow along after the incident.

## Be the catalyst in a junior engineer's career

_[Amber Shand](https://twitter.com/amberleetech) and [Jessie Auguste](https://twitter.com/_jessie_belle)_

There are four stages to a person's career in a company:

1. Attraction
1. Onboarding
1. Development
1. Retention

The [Tech Talent Charter](https://www.techtalentcharter.co.uk/home) is a non-profit organisation aiming to improve
inequality, diversity and inclusion in the UK tech sector.

Mentors vs Buddies vs Sponsors

Mentors should avoid spoon-feeding people - teach people how to teach themselves.

Buddies should cooperate with them. Be a safe person for them to discuss things with.

Sponsors should aim to identify and promote high performers.

Provide opportunities for people to add value beyond adding code.

## Compassionate Refactoring

_[Clare Sudbery](https://twitter.com/claresudbery)_

Refactoring should make things...

* easier to understand.
* so they can fit into our heads.
* cheaper to modify.

Move in tiny steps, and don't refactor code that isn't testable.

Why do people not refactor?

* External pressure.
* Unrealistic deadlines.
* Impatience.
* Seeking perfection.

This leads to guilt... shame... and despair.

This makes you feel like you're not as good as the book you read, or the speaker you saw.

It makes you want to hide bad code.

It makes you try a big bang refactor, which doesn't work.

We're in a knowledge industry and yet we find it hard to ask permission to spend time
to think and analyse.

People in leadership feel like they need to give the impression of everything they do
being great. This makes junior engineers feel bad.

We need to allow time because we are fallible.

Sculptors start a raw material and remove bits. Writers and coders need to create the raw
material so we can start editing - the first draft.

Something that is slightly improved is better than something that has been destroyed to try
and make it perfect.

Learn how to make the tiniest improvement that keeps the tests green.

Seek the joy of coding and of doing a good job. People who enjoy their work are much more effective.

# Skiller Whale Coding Competition

During the conference [Skiller Whale](http://skillerwhale.com) were running a coding competition
where the top three entries would win an Oculus Quest 2. The challenge was twofold. Firstly you
needed to write an SQL query processing some customer data. The second part was to automate the
submission so you could submit it quickly enough.

The first part was pretty fiddly to get right. There was a customer table and an orders table. The
problem was to calculate the average rank of customers over a period, where customers are ranked
daily based on the amount spent, including on days when they didn't spend anything. Ranking customers
is easy enough using the [rank function](https://www.postgresql.org/docs/current/tutorial-window.html).
The challenge comes from including customers on days they didn't order anything. This requires a `full
outer join` between a table of dates and the customers and then left joining onto the orders table.

Each time you submitted an entry you were given a different date range and target rank to return. The
second part of the challenge is to automate the submission so you can submit in less than one second.
Luckily for me, only two people completed this part, leaving the third spot open to the person with the
most efficient query. I managed to sneak into third place by replacing the date table, which initially
I was doing this by running a distinct over the dates in the order table (requiring a full scan of the table),
with the [`generate_series` function](https://www.postgresql.org/docs/current/functions-srf.html) which
is much more efficent.

I'll write a review of the Quest 2 when I've played with it a bit, thanks [Skiller Whale](http://skillerwhale.com)!

I've included the SQL I submitted below, just in case anyone is interested.

{% highlight sql %}
with sales_by_day as
    (select dates.date, customers.id as customer_id, name,
            rank () over
                (partition by dates.date
                    order by coalesce(sum(amount), 0) desc)
                as pos
        from customers
             full outer join
                (select @start_date
                        + (n || ' day')::interval as date
                    from generate_series(0, 30) n) as dates
                on 1=1
             left join orders on
                orders.date >= @start_date
                and orders.date <= @end_date
                and orders.date=dates.date
                and orders.customer_id=customers.id
        group by dates.date, customers.id, name)
select name, avg_pos from (
    select name, avg(pos) as avg_pos,
           rank () over (order by avg(pos) asc) as avg_rank
        from sales_by_day group by customer_id, name
) as avg_rank
    where avg_rank=@rank limit 1
{% endhighlight %}

![LeadDev London 2022](/assets/leaddev2022_room.jpeg)