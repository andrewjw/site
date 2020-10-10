---
title: Two Dimensional Dates
layout: post
date: 2020-10-10
tags:
- covid19
- data structures
permalink: "/2020/10/10/two-dimensional-dates/"
flickr_user: 'https://www.flickr.com/photos/wikidave/'
flickr_username: Dave Crosby
flickr_image: 'https://live.staticflickr.com/7238/7386337594_0e1821fe71_w.jpg'
flickr_imagelink: 'https://www.flickr.com/photos/wikidave/7386337594/'
flickr_imagename: '159/365+1 Clipboard'
---
Last week the UK government announced [more than 12,000 cases](https://www.bbc.co.uk/news/health-54404561)
of COVID-19 - more than double the number from the day before. This increase was accompanied by the following
message on the [Government's Data Dashboard](https://coronavirus.data.gov.uk/).

> Due to a technical issue, which has now been resolved, there has been a delay in publishing a number of
> COVID-19 cases to the dashboard in England. This means the total reported over the coming days will
> include some additional cases from the period between 24 September and 1 October, increasing the number
> of cases reported.

This turned out to be an issue with the reporting of positive tests caused by a limit in Excel. An interesting
part of the story is the way it was initially reported in the media. Their focus is on the number of the cases
reported each day, which due to the delay in processing tests is not accurate normal, but with this delay is
a pretty meaningless number. The key measure used to make important decisions is the rolling average of new
case over the last seven days, and with this number you can't at a glance know how the average is changing.

What is particularly odd, is that it turns out that the government do publish the number of positive cases by
the date the sample was taken. It's just that for the last few days the media narrative has been "huge number
of cases", even though that's largely an artefact of the old incorrect data. Sure they're high, but they went
up a week before, not last Saturday.
<!--more-->

Now, I'm not a virologist, a sociologist or a politician. I am a developer, and this got me thinking about
how to design data structures for time-series data. It's tempting to think of time-series data as consisting of
a pair of values - the metric, and the date the value applies to. In the example above this would be the number
of positive tests, and the date the sample was taken. As we've seen so clearly over the last few days
this time-series is not immutable, and the history can and will change as new information becomes available.

A better way to think about the data is as a triple - the metric, the date the value applies to, and the date
we knew about the data point. Depending on what you want to do with the data the second date could be part of
the primary key. In many cases you only ever want to know what is our best view of the history - in this case
just having a `last_modified` date is probably enough. Just having a date that represents when the value was
last updated shows that the history is mutable.

In some cases though, you want to be able to 're-run' history, and in that case, making the `date_known` part
of your primary key gives you a two-dimensional view of the data. On one axis you have the date the value
applies to, and on the other, it's the date that we knew about that value. This allows you to ask on this
date, what was our view of the data? If you're training a machine learning model or trying to do any sort
of prediction, it's crucial that you don't train it on data that you didn't know at the time. It'd very easy
to think you can predict the stock market if you train your model on a complete history of shares prices.

Taking the COVID data as an example, the media seem to be relying on an immutable time-series of the difference
in the total number of cases each day - this is an immutable series of `(date, value)` pairs. The Government's
Data dashboard shows the number of positive tests by day the sample was taken - this is a mutable series of
`(date, value, last_modified)` triples. The most flexible data structure would be an immutable series of
`(date, date_known, value)` triples. This lets you generate both the media's and the Government's data, as well
as other questions such as how long is it taking on average for a test to be reported? Or, how much higher
is the final value compared to what was initially reported?

Timeseries data is all around us, and it's easy to think that history doesn't change. Unless you're measuring
something directly then all you have is your best view of the data at a given point in time. Expecting that
to not change is both likely to be incorrect, but will also prevent you from asking interesting questions of
your data. So the next time you're building a time-series, try to think in two dimensions.
