---
layout: post
title: Unittesting QSyntaxHighlighter
date: 2011-02-16 14:04:09.000000000 +01:00
tags:
  - programming
  - qt
  - unitesting
  - unittest
  - djangode
permalink: /2011/02/16/unittesting-qsyntaxhighlighter/
flickr_user: 'https://www.flickr.com/photos/alisdair/'
flickr_username: "alisdair"
flickr_image: 'https://live.staticflickr.com/48/135306281_06746ebf30_w.jpg'
flickr_imagelink: 'https://www.flickr.com/photos/alisdair/135306281/'
flickr_imagename: 'Testing 1, 2, 3'
---
I'm using [test driven development](http://en.wikipedia.org/wiki/Test-driven_development) while
building my pet project, [DjangoDE](http://www.djangode.com). A key part of an IDE is the syntax
highlighting of the code in the editor, so that's one area where I've been trying to build up the test suite.

To test the syntax highlighter the obvious approach is to send the right events to write some code into the
editor the check the colour of the text. Although the [QT documentation](http://doc.qt.nokia.com/)
is usually excellent, it doesn't go into enough detail on the implementation of the syntax highlighting
framework to enable you to query the colour of the text. In this post I'll explain how the colour of text is
stored, and how you can query it.

A syntax highlighting editor is normally implemented using a
[QPlainTextEdit](http://doc.qt.nokia.com/qplaintextedit.html) widget. This object provides the user
interface to the editor and manages the display of the text. The widget contains a
[QTextDocument](http://doc.qt.nokia.com/qtextdocument.html) instance, which stores the text. To add
syntax highlighting you derive a class from
[QSyntaxHighlighter](http://doc.qt.nokia.com/qsyntaxhighlighter.html) then instantiate it, passing
the document instance as the parameter to the constructor. This is explained in detail in the
[syntax highlighter example](http://doc.qt.nokia.com/4.7/richtext-syntaxhighlighter.html).

The document stores the text as a sequence of [QTextBlock](http://doc.qt.nokia.com/qtextblock.html)
objects. These store the text as well as the formatting information used to display it. You might think that
you can just call `QTextBlock::charFormat` to get the colour of the text. Unfortunately it's not that
simple as the format returned by that call is the colour that you've explicitly set, not the syntax highlight
colour.

Each QTextBlock is associated with a [QTextLayout](http://doc.qt.nokia.com/qtextlayout.html) object
that controls how the block is rendered. Each layout has a list of
[FormatRange](http://doc.qt.nokia.com/4.7/qtextlayout-formatrange.html) objects, accessible using
the `additionalFormats` method. It is this list that the QSyntaxHighlighter sets to specify the colour
of the text.

Now we know where the colour information is stored, we can find out what colour a particular character will
be. Firstly you need to find out which `QTextBlock` the text you want is. In a plain text document each
line is represented by a separate block, so this is quite straightforward. You then get the list of
`FormatRanges` and then iterate through, checking to see if the character you want is between
`format_range.start` and `format_range.start + format_range.length`

For an example of this you can check out the test file from DjangoDE [here](http://code.google.com/p/djangode/source/browse/trunk/djangode/tests/gui/highlighters/python.py)
