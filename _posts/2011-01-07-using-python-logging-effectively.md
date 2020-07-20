---
layout: post
title: Using Python Logging Effectively
date: 2011-01-07 12:00:00.000000000 +01:00
tags:
  - code
  - logging
  - programming
  - python
permalink: /2011/01/07/using-python-logging-effectively/
---
If you're writing a Python program that doesn't have a text-based user interface (either it's a GUI or runs as part of another program, e.g. a webserver) then you should avoid using the <tt>print</tt> statement. It's tempting to use <tt>print</tt> to fill the console with information about what your program is up to. For code of any size though, this quickly devolves into a hard to navigate mess.

Python's standard library contains a module, <a href="http://docs.python.org/library/logging.html"><tt>logging</tt></a>, that lets you write code to log as much information as you like and configure what you bits you are interested in at runtime.

There are two concepts that you need to understand with logging. Firstly there is the logging level. This is how you determine how important the message is. The levels range from <tt>debug</tt> as the least important, through <tt>info</tt>, <tt>warning</tt>, <tt>error</tt>, <tt>critical</tt> to <tt>exception</tt>, the most important. Secondly there is the logger. This allows you divide your messages into groups depending on the part of your code they relate to. For example, you might have a <tt>gui</tt> logger and a <tt>data</tt> logger.n
The <tt>logging</tt> comes with a series of module level functions by each of the names of the logging levels. These make it quick and easy to log a message using the default logger.

    logging.debug(&quot;Debug message&quot;)
    logging.error(&quot;Error retrieving %s&quot;, url)

The second of these two lines has more than one argument. In this case the logging module will treat the first argument as a format string and the rest as arguments to the format, so that line equivalent to this one.

    logging.error(&quot;Error retrieving %s&quot; % (url, ))

If you try to treat the logging code like you would a print statement and write <tt>logging.error("Error retrieving", url)</tt> then you'll get the following, very unhelpfui, error message.

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

Notice how this exception doesn't tell you where the offending logging statement is in your code! Now you know the type of error that will cause this that will help in tracking the problem down, but there is more than can be done to help you find it. The logging library allows you to specify a global error handle, which combined with the print stack trace function will give you a much better error message.

    import logging
    import traceback
    def handleError(self, record):
        traceback.print_stack()
    logging.Handler.handleError = handleError

Loggers are created by calling <tt>logging.getLogger('loggername')</tt>. This returns an object with the same set of log level functions as the module, but which can be controlled independently. For example:

    gui_log = logging.getLogger('gui')
    gui_log.debug(&quot;created window&quot;)
    data_log = logging.getLogger('gui')
    data_log.debug(&quot;loaded file&quot;)

Where this comes in really handy is when you set the level of messages that you want to see independently for each logger. In the next code block we set the logging module so we'll see lots of debugging messages from the GUI and only errors from the data layer. Although here we're setting the levels directly in code, it's not a big jump to make them configurable using a command line option.

    gui_log.setLevel(logging.DEBUG)
    data_log.setLevel(logging.ERROR)

The logging module also lets you configure how your messages are formatted, and to direct them to files rather than the console. Hopefully this short guide is useful, let me know in the comments!
