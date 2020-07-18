---
layout: post
title: Unittesting QSyntaxHighlighter
date: 2011-02-16 13:20:24.000000000 +00:00
type: post
parent_id: '0'
published: true
password: ''
status: publish
categories:
- djangode
tags:
- programming
- qt
- unitesting
- unittest
meta:
  _edit_last: '364050'
  _wpas_done_twitter: '1'
author:
  login: andrewjw
  email: andrewjwilkinson@gmail.com
  display_name: Andrew Wilkinson
  first_name: Andrew
  last_name: Wilkinson
permalink: "/2011/02/16/unittesting-qsyntaxhighlighter/"
---
<a href="http://www.flickr.com/photos/alisdair/135306281/"><img src="{{ site.baseurl }}/assets/135306281_06746ebf30_m.jpg" alt="Testing 1, 2, 3 by alisdair" style="float:right;border:0;" /></a>I'm using <a href="http://en.wikipedia.org/wiki/Test-driven_development">test driven development</a> while building my pet project, <a href="http://www.djangode.com">DjangoDE</a>. A key part of an IDE is the syntax highlighting of the code in the editor, so that's one area where I've been trying to build up the test suite.n
To test the syntax highlighter the obvious approach is to send the right events to write some code into the editor the check the colour of the text. Although the <a href="http://doc.qt.nokia.com/">QT documentation</a> is usually excellent, it doesn't go into enough detail on the implementation of the syntax highlighting framework to enable you to query the colour of the text. In this post I'll explain how the colour of text is stored, and how you can query it.n
A syntax highlighting editor is normally implemented using a <a href="http://doc.qt.nokia.com/qplaintextedit.html">QPlainTextEdit</a> widget. This object provides the user interface to the editor and manages the display of the text. The widget contains a <a href="http://doc.qt.nokia.com/qtextdocument.html">QTextDocument</a> instance, which stores the text. To add syntax highlighting you derive a class from <a href="http://doc.qt.nokia.com/qsyntaxhighlighter.html">QSyntaxHighlighter</a> then instantiate it, passing the document instance as the parameter to the constructor. This is explained in detail in the <a href="http://doc.qt.nokia.com/4.7/richtext-syntaxhighlighter.html">syntax highlighter example</a>.n
The document stores the text as a sequence of <a href="http://doc.qt.nokia.com/qtextblock.html">QTextBlock</a> objects. These store the text as well as the formatting information used to display it. You might think that you can just call <tt>QTextBlock::charFormat</tt> to get the colour of the text. Unfortunately it's not that simple as the format returned by that call is the colour that you've explicitly set, not the syntax highlight colour.n
Each QTextBlock is associated with a <a href="http://doc.qt.nokia.com/qtextlayout.html">QTextLayout</a> object that controls how the block is rendered. Each layout has a list of <a href="http://doc.qt.nokia.com/4.7/qtextlayout-formatrange.html">FormatRange</a> objects, accessible using the <tt>additionalFormats</tt> method. It is this list that the QSyntaxHighlighter sets to specify the colour of the text.n
Now we know where the colour information is stored, we can find out what colour a particular character will be. Firstly you need to find out which <tt>QTextBlock</tt> the text you want is. In a plain text document each line is represented by a separate block, so this is quite straightforward. You then get the list of <tt>FormatRanges</tt> and then iterate through, checking to see if the character you want is between <tt>format_range.start</tt> and <tt>format_range.start + format_range.length</tt>n
For an example of this you can check out the test file from DjangoDE <a href="http://code.google.com/p/djangode/source/browse/trunk/djangode/tests/gui/highlighters/python.py">here</a>n
<hr />
Photo of <a href="http://www.flickr.com/photos/alisdair/135306281/">Testing 1, 2, 3</a> by <a href="http://www.flickr.com/photos/alisdair/">alisdair</a>.n