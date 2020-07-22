---
layout: post
title: Deadlock On Exit With PySide And QFileSystemWatcher
date: 2011-03-14 14:04:09.000000000 +01:00
type: post
tags:
  - pyqt
  - pyside
  - python
  - qt
  - djangode
permalink: /2011/03/14/deadlock-on-exit-with-pyside-and-qfilesystemwatcher/
flickr_user: 'https://www.flickr.com/photos/bohman/'
flickr_username: "Linus Bohman"
flickr_image: 'https://live.staticflickr.com/97/210977249_da533e62a4_w.jpg'
flickr_imagelink: 'https://www.flickr.com/photos/bohman/210977249/'
flickr_imagename: 'Keys.'
---
Last year Nokia started developing their own Python bindings for Qt,
<a href="http://www.pyside.org">PySide</a>, when they couldn't persuade Riverbank Computing to relicense
<a href="http://www.riverbankcomputing.co.uk/software/pyqt/intro">PyQt</a> under a more liberal license. While
developing <a href="http://www.djangode.com">DjangoDE</a> I made the choice of which library to use
configurable. When running under PyQt everything worked fine, but when using PySide the program hung on exit.

Using gdb to see where it was hanging points to
<a href="http://doc.qt.nokia.com/4.7/qfilesystemwatcher.html">QFileSystemWatcher</a>, which has the following comment in the destructor.

    Note: To avoid deadlocks on shutdown, all instances of QFileSystemWatcher need to be destroyed
    before QCoreApplication. Note that passing QCoreApplication::instance() as the parent object
    when creating QFileSystemWatcher is not sufficient.

The following code will demonstrate the issue.

{% highlight python %}
import sys
#from PyQt4 import QtGui
from PySide import QtGui
app = QtGui.QApplication(sys.argv)
file_browser = QtGui.QTreeView()
file_model = QtGui.QFileSystemModel()
file_model.setRootPath(&quot;/&quot;)
file_browser.setModel(file_model)
file_browser.show()
sys.exit(app.exec_())
{% endhighlight %}

As the comment says, we need to ensure that the <tt>QFileSystemWatcher</tt> object, which is created by
<tt>QFileSystemModel</tt>, is destroyed before <tt>QApplication</tt>. To do this we can connect to the
<tt>lastWindowClosed</tt> and ensure that the <tt>QFileSystemModel</tt> is fully destroyed.

{% highlight python %}
import gcn
def app_quit():
     global file_browser
     file_browser = None
     gc.collect()
app.lastWindowClosed.connect(app_quit)
{% endhighlight %}

It's not clear why this code would work on PyQt and not PySide, but it is clearly related to the order the
objects are deleted. Given the comment in the Qt documentation though you should probably not rely on it
working on PyQt and ensure yourself that the <tt>QApplication</tt> is the last Qt object to be destroyed.
