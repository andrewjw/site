---
layout: post
title: Using Python Logging Effectively
date: 2011-01-07 13:09:14.000000000 +00:00
type: post
parent_id: '0'
published: true
password: ''
status: publish
categories:
- python
tags:
- code
- logging
- programming
meta:
  _edit_last: '364050'
  _wpas_done_twitter: '1'
  _oembed_9901351c9189e43c8dfca4e71322f339: "{{unknown}}"
  _oembed_12a1ae63c005ec9572550c758b01a910: "{{unknown}}"
  _oembed_0ff2a3dcc5f4ec8657fd634560971516: "{{unknown}}"
  _oembed_b664cf6de325b62d3f8247c047df5d9d: "{{unknown}}"
  _oembed_a61af4d04452fabc1b9e254ab31f6104: "{{unknown}}"
  _oembed_2e710c66dde610d2dad6ed6197be6b16: "{{unknown}}"
  _oembed_f8f36f3d783004d0006d560584876e89: "{{unknown}}"
  _oembed_f4c3a1a7f92dfaf3b1ded368bd0b60d1: "{{unknown}}"
  _oembed_78b9e126c8edd189b9fe71bc628c3eb0: "{{unknown}}"
  _oembed_e7e238c2b283f54017859cd5d56b9d3c: "{{unknown}}"
author:
  login: andrewjw
  email: andrewjwilkinson@gmail.com
  display_name: Andrew Wilkinson
  first_name: Andrew
  last_name: Wilkinson
permalink: "/2011/01/07/using-python-logging-effectively/"
---
If you're writing a Python program that doesn't have a text-based user interface (either it's a GUI or runs as part of another program, e.g. a webserver) then you should avoid using the <tt>print</tt> statement. It's tempting to use <tt>print</tt> to fill the console with information about what your program is up to. For code of any size though, this quickly devolves into a hard to navigate mess.n
Python's standard library contains a module, <a href="http://docs.python.org/library/logging.html"><tt>logging</tt></a>, that lets you write code to log as much information as you like and configure what you bits you are interested in at runtime.n
There are two concepts that you need to understand with logging. Firstly there is the logging level. This is how you determine how important the message is. The levels range from <tt>debug</tt> as the least important, through <tt>info</tt>, <tt>warning</tt>, <tt>error</tt>, <tt>critical</tt> to <tt>exception</tt>, the most important. Secondly there is the logger. This allows you divide your messages into groups depending on the part of your code they relate to. For example, you might have a <tt>gui</tt> logger and a <tt>data</tt> logger.n
The <tt>logging</tt> comes with a series of module level functions by each of the names of the logging levels. These make it quick and easy to log a message using the default logger.n
[code lang="python"]<br />
logging.debug(&quot;Debug message&quot;)<br />
logging.error(&quot;Error retrieving %s&quot;, url)<br />
[/code]n
The second of these two lines has more than one argument. In this case the logging module will treat the first argument as a format string and the rest as arguments to the format, so that line equivalent to this one.n
[code lang="python"]<br />
logging.error(&quot;Error retrieving %s&quot; % (url, ))<br />
[/code]n
If you try to treat the logging code like you would a print statement and write <tt>logging.error("Error retrieving", url)</tt> then you'll get the following, very unhelpfui, error message.n
<pre>
Traceback (most recent call last):
  File "/usr/lib/python2.6/logging/__init__.py", line 776, in emit
    msg = self.format(record)
  File "/usr/lib/python2.6/logging/__init__.py", line 654, in format
    return fmt.format(record)
  File "/usr/lib/python2.6/logging/__init__.py", line 436, in format
    record.message = record.getMessage()
  File "/usr/lib/python2.6/logging/__init__.py", line 306, in getMessage
    msg = msg % self.args
TypeError: not all arguments converted during string formatting
</pre>
Notice how this exception doesn't tell you where the offending logging statement is in your code! Now you know the type of error that will cause this that will help in tracking the problem down, but there is more than can be done to help you find it. The logging library allows you to specify a global error handle, which combined with the print stack trace function will give you a much better error message.n
[code lang="python"]<br />
import logging<br />
import tracebackn
def handleError(self, record):<br />
    traceback.print_stack()<br />
logging.Handler.handleError = handleError<br />
[/code]n
Loggers are created by calling <tt>logging.getLogger('loggername')</tt>. This returns an object with the same set of log level functions as the module, but which can be controlled independently. For example:n
[code lang="python"]<br />
gui_log = logging.getLogger('gui')<br />
gui_log.debug(&quot;created window&quot;)n
data_log = logging.getLogger('gui')<br />
data_log.debug(&quot;loaded file&quot;)<br />
[/code]n
Where this comes in really handy is when you set the level of messages that you want to see independently for each logger. In the next code block we set the logging module so we'll see lots of debugging messages from the GUI and only errors from the data layer. Although here we're setting the levels directly in code, it's not a big jump to make them configurable using a command line option.n
[code lang="python"]<br />
gui_log.setLevel(logging.DEBUG)<br />
data_log.setLevel(logging.ERROR)<br />
[/code]n
The logging module also lets you configure how your messages are formatted, and to direct them to files rather than the console. Hopefully this short guide is useful, let me know in the comments!n
