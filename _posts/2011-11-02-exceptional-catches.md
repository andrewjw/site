---
layout: post
title: Exceptional Catches
date: 2011-11-02 12:00:18.000000000 +00:00
type: post
parent_id: '0'
published: true
password: ''
status: publish
categories:
- python
tags:
- exceptions
meta:
  _edit_last: '364050'
  _wpas_done_twitter: '1'
author:
  login: andrewjw
  email: andrewjwilkinson@gmail.com
  display_name: Andrew Wilkinson
  first_name: Andrew
  last_name: Wilkinson
permalink: "/2011/11/02/exceptional-catches/"
---
<a href="http://www.flickr.com/photos/biggleswadeblue/3206950603/"><img style="float:right;border:0;" src="{{ site.baseurl }}/assets/3206950603_b6449c2067_m.jpg" alt="Throw In" /></a>Recently I was taking part in a review of some Python code. One aspect of the code really stuck out to me. It's not a structural issue, but a minor change in programming style that can greatly improve the maintainability of the code.n
The code in general was quite good, but a code snippet similar to that given below jumped right to the top of my list of things to be fixed. Why is this so bad? Let us first consider what exceptions are and why you might use them in Python.n
[code language="python"]<br />
try:<br />
    // code<br />
except Exception, e:<br />
    // error handling code<br />
[/code]n
Exceptions are a way of breaking out the normal program flow when an 'exceptional' condition arises. Typically this is used when errors occur, but exceptions can also be used as an easy way to break out of normal flow during normal but unusual conditions. In a limited set of situations it can make program flow clearer.n
What does this code do though? It catches all exceptions, runs the error handling code and continues like nothing has happened. In all probability it's only one or two errors that are expected and should be handled. Any other errors should be passed on a cause the program to actually crash so it can be debugged properly.n
Let's consider the following code:n
[code language="python"]<br />
analysis_type = 1<br />
try:<br />
    do_analysis(analysis_typ)<br />
except Exception, e:<br />
    cleanup()<br />
[/code]n
This code has a bug, the missing <tt>e</tt> in the <tt>do_analysis</tt> call. This will raise a <tt>NameError</tt> that will be immediately captured and hidden. Other, more complicated errors could also occur and be hidden in the same way. This sort of masking will make tracking down problems like this very difficult.n
To improve this code we need to consider what errors we expect the <tt>do_analysis</tt> function to raise and what we want to handle. In the ideal case it would raise an <tt>AnalysisError</tt> and then we would catch that.n
[code language="python"]<br />
analysis_type = 1<br />
try:<br />
    do_analysis(analysis_typ)<br />
except AnalysisError, e:<br />
    cleanup()<br />
[/code]n
In the improved code the <tt>NameError</tt> will pass through and be picked up immediately. It is likely that the <tt>cleanup</tt> function needs to be run whether or not an error has occurred. To do that we can move the call into a <tt>finally</tt> block.n
[code language="python"]<br />
analysis_type = 1<br />
try:<br />
    do_analysis(analysis_typ)<br />
except AnalysisError, e:<br />
    // display error message<br />
finally:<br />
    cleanup()<br />
[/code]n
This allows us to handle a very specific error and ensure that we clean up whatever error happens. Sometimes cleaning up whatever the exception (or in the event of no exception) is required, and in this case the finally block, which is always run, is the right place for this code.n
Let's now consider a different piece of code.n
[code language="python"]<br />
try:<br />
    do_analysis(analysis_types[index])<br />
except KeyError:<br />
    // display error message<br />
[/code]n
We're looking up the parameter to <tt>do_analysis</tt> in a dictionary and catching the case where <tt>index</tt> doesn't exist. This code is also capturing too much. Not because the exception is too general, but because there is too much code in the <tt>try</tt> block.n
The issue with this code is what happens if <tt>do_analysis</tt> raises a <tt>KeyError</tt>? To capture the exceptions that we're expecting we need to only wrap the dictionary lookup in and not catch anything from the analysis call.n
[code language="python"]<br />
try:<br />
    analysis_type = analysis_types[index]<br />
except KeyError:<br />
    // display error message<br />
finally:<br />
    do_analysis(analysis_type)<br />
[/code]n
So, if I'm reviewing your code don't be afraid to write a few extra lines in order to catch the smallest, but correct, set of exceptions.n
<hr />
Photo of <a href="http://www.flickr.com/photos/biggleswadeblue/3206950603/">Throw In</a> by <a href="http://www.flickr.com/photos/biggleswadeblue/">Nick Treby</a>.n
