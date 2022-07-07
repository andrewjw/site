---
layout: post
title: LeadDev London 2022 Day 2
date: 2022-06-23
tags: conference leaddev
permalink: "/2022/06/23/leadev-london-2022-day-2/"
image: leaddev2022_welcome.jpeg
image_title: Welcome To LeadDev London 2022
---
Recently I was lucky enough to go to LeadDev London. You can read about my general thoughts, and the first
day of talks, [here](https://www.theandrewwilkinson.com/2022/06/17/leadev-london-2022-day-1/). This
post covers the second day.

The following is a summary of my notes from each talk. Any mistakes, errors or things that don't
make sense are entirely my fault. Hopefully this will provide a flavour of each talk and inspire
you to watch the ones that interest you the most to get the full story.
<!-- more -->

## Why we are writing a monolith, not a microservice

_[Supriya Srivatsa](https://supriyasrivatsa.com/)_

xxx

## A Commune in the Ivory Tower? - A new approach to architecture decisions

_[Andrew Harmel-Law](https://twitter.com/al94781)_

xxx

## Sorry... you go ahead. The art of making space and claiming space in meetings

_[Jemma Bolland](https://twitter.com/jemolova)_

xxx

## Using incidents to level-up your teams

_[Lisa Karlin Curtis](https://twitter.com/paprikati_eng)_

xxx

## Be the catalyst in a junior engineer's career

_[Amber Shand](https://twitter.com/amberleetech) and [Jessie Auguste](https://twitter.com/_jessie_belle)_ 

xxx

## Compassionate Refactoring

_[Clare Sudbery](https://twitter.com/claresudbery)_

xxx

# Skiller Whale Coding Competition

During the conference [Skiller Whale](http://skillerwhale.com) were running a coding competition
where the top three entries would win an Oculus Quest 2. The challenge was two fold. Firstly you
needed to write an SQL query processing some customer data. The second part was to automate the
submission so you could submit it quickly enough.

The first part was pretty fiddly to get right. There was a customer table, and an orders table. The
problem was to calculate the average rank of customers over a period, where customers are ranked
daily based on the amount spend, including on days when they didn't spend anything. Ranking customers
is easy enough using the [rank function](https://www.postgresql.org/docs/current/tutorial-window.html).
The challenge comes from including customers on days they didn't order anything. This requires a `full
outer join` between a table of dates and the customers, and then left joining onto the orders table.

Each time you submitted an entry you were given a different date range and target rank to return. The
second part of the challenge is to automate the submission so you can submit in less than one second.
Luckily for me only two people completed this part, leaving the third spot open to the person with the
most efficient query. I managed to sneak into third place by replacing the date table, which initially
I was doing by running a distinct over the dates in the order table (requiring a full scan of the table),
with the [`generate_series` function](https://www.postgresql.org/docs/current/functions-srf.html) which
is much more efficent.

I'll write a review of the Quest 2 after it arrives, thanks Skiller Whale!

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