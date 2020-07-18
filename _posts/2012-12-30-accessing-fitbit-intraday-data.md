---
layout: post
title: Accessing FitBit Intraday Data
date: 2012-12-30 13:22:03
tags:
- python
- fitbit
- github
- library
- programming
slug: "accessing-fitbit-intraday-data"
permalink: "/2012/12/30/accessing-fitbit-intraday-data/"
flickr_user: 'http://www.flickr.com/photos/eulothg/'
flickr_username: Glenn Euloth
flickr_image: 'https://live.staticflickr.com/7186/6844568450_8b7d3ef8c8_w.jpg'
flickr_imagelink: 'http://www.flickr.com/photos/eulothg/6844568450/'
flickr_imagename: Jogging
---
For Christmas my wife and I brought each other a new <a href="http://www.amazon.co.uk/gp/product/B0096NXKAE/ref=as_li_tf_tl?ie=UTF8&amp;tag=indiegicouk-21&amp;linkCode=as2&amp;camp=1634&amp;creative=6738&amp;creativeASIN=B0096NXKAE">FitBit One device</a> (Amazon affiliate link included). These are small fitness tracking devices that monitor the number of steps you take, how high you climb and how well you sleep. They're great for providing motivation to walk that extra bit further, or to take the stairs rather than the lift.

I've only had the device for less than a week, but already I'm feeling the benefit of the gamification on <a href="http://www.fitbit.com">FitBit.com</a>. As well as monitoring your fitness it also provides you with goals, achievements and competitions against your friends. The big advantage of the FitBit One over the previous models is that it syncs to recent iPhones, iPads, as well as some Android phones. This means that your computer doesn't need to be on, and often it will sync without you having to do anything. In the worst case you just have to open the FitBit app to update your stats on the website. Battery life seems good, at about a week.

The FitBit apps sync your data directly to FitBit.com, which is great for seeing your progress quickly. They also provide an <a href="https://wiki.fitbit.com/display/API/Fitbit+API">API</a> for developers to provide interesting ways to process the data captured by the FitBit device. One glaring omission from the API is any way to get access to the minute by minute data. For a fee of $50 per year you can become a <a href="http://www.fitbit.com/premium/export">Premium member</a> which allows you do to a CSV export of the raw data. Holding the data, collected by a user hostage is deeply suspect and FitBit should be ashamed of themselves for making this a paid for feature. I have no problem with the rest of the features in the Premium subscription being paid for, but your own raw data should be freely available.

The FitBit API does have the ability to give you the intraday data, but this is not part of the open API and instead is part of the 'Partner API'. This does not require payment, but you do need to explain to FitBit why you need access to this API call and what you intend to do with it. I do not believe that they would give you access if your goal was to provide a free alternative to the Premium export function.

So, has the free software community provided a solution? A quick search revealed that the GitHub user <a href="https://github.com/wadey">Wadey</a> had created a <a href="https://github.com/wadey/python-fitbit">library</a> that uses the urls used by the graphs on the FitBit website to extract the intraday data. Unfortunately the library hadn't been updated in the last three years and a change to the FitBit website had broken it.

Fortunately the changes required to make it work are relatively straightforward, so a fixed version of the library is now available as <a href="https://github.com/andrewjw/python-fitbit">andrewjw/python-fitbit</a>. The old version of the library relied on you logging into to FitBit.com and extracting some values from the cookies. Instead I take your email address and password and fake a request to the log in page. This captures all of the cookies that are set, and will only break if the log in form elements change.

Another change I made was to extend the example <tt>dump.py</tt> script. The previous version just dumped the previous day's values, which is not useful if you want to extract your entire history. In my new version it exports data for every day that you've been using your FitBit. It also incrementally updates your data dump if you run it irregularly.

If you're using Windows you'll need both <a href="http://www.python.org">Python</a> and <a href="http://windows.github.com/">Git</a> installed. Once you've done that check out my repository at <a href="https://github.com/andrewjw/python-fitbit">github.com/andrewjw/python-fitbit</a>. Lastly, in the newly checked out directory run <tt>python examples/dump.py &lt;email&gt; &lt;password&gt; &lt;dump directory&gt;</tt>.
