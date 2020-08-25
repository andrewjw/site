---
layout: post
title: Exceptional Catches
date: 2011-11-02 12:00:18.000000000 +00:00
tags:
- exceptions
- python
permalink: "/2011/11/02/exceptional-catches/"
flickr_user: 'http://www.flickr.com/photos/biggleswadeblue/'
flickr_username: "Biggleswade Blue"
flickr_image: 'https://live.staticflickr.com/3382/3206950603_b6449c2067_w.jpg'
flickr_imagelink: 'http://www.flickr.com/photos/biggleswadeblue/3206950603/'
flickr_imagename: 'Throw In'
---
Recently I was taking part in a review of some Python code. One aspect of the code really stuck out to me.
It's not a structural issue, but a minor change in programming style that can greatly improve the
maintainability of the code.

The code in general was quite good, but a code snippet similar to that given below jumped right to the top of
my list of things to be fixed. Why is this so bad? Let us first consider what exceptions are and why you might
use them in Python.

```python
try:
    // code
except Exception, e:
    // error handling code
```

 Exceptions are a way of breaking out the normal program flow when an 'exceptional' condition arises.
Typically this is used when errors occur, but exceptions can also be used as an easy way to break out of
normal flow during normal but unusual conditions. In a limited set of situations it can make program flow
clearer.

What does this code do though? It catches all exceptions, runs the error handling code and continues like
nothing has happened. In all probability it's only one or two errors that are expected and should be handled.
Any other errors should be passed on a cause the program to actually crash so it can be debugged properly.
Let's consider the following code:

```python
analysis_type = 1
try:
    do_analysis(analysis_typ)
except Exception, e:
    cleanup()
```

 This code has a bug, the missing `e` in the `do_analysis` call. This will raise a
`NameError` that will be immediately captured and hidden. Other, more complicated errors could also
occur and be hidden in the same way. This sort of masking will make tracking down problems like this very
difficult.

To improve this code we need to consider what errors we expect the `do_analysis` function to raise and
what we want to handle. In the ideal case it would raise an `AnalysisError` and then we would catch
that.

```python
analysis_type = 1
try:
    do_analysis(analysis_typ)
except AnalysisError, e:
    cleanup()
```

 In the improved code the `NameError` will pass through and be picked up immediately. It is likely
that the `cleanup` function needs to be run whether or not an error has occurred. To do that we can
move the call into a `finally` block.

```python
analysis_type = 1
try:
    do_analysis(analysis_typ)
except AnalysisError, e:
    // display error message
finally:
    cleanup()
```

 This allows us to handle a very specific error and ensure that we clean up whatever error happens. Sometimes
cleaning up whatever the exception (or in the event of no exception) is required, and in this case the
finally block, which is always run, is the right place for this code.

Let's now consider a different piece of code.

```python
try:
    do_analysis(analysis_types[index])
except KeyError:
    // display error message
```

 We're looking up the parameter to `do_analysis` in a dictionary and catching the case where
`index` doesn't exist. This code is also capturing too much. Not because the exception is too general,
but because there is too much code in the `try` block.

The issue with this code is what happens if `do_analysis` raises a `KeyError`? To capture the
exceptions that we're expecting we need to only wrap the dictionary lookup in and not catch anything from the
analysis call.

```python
try:
    analysis_type = analysis_types[index]
except KeyError:
    // display error message
finally:
    do_analysis(analysis_type)
```

 So, if I'm reviewing your code don't be afraid to write a few extra lines in order to catch the smallest,
but correct, set of exceptions.
