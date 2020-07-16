---
layout: post
title: Deadlock On Exit With PySide And QFileSystemWatcher
date: 2011-03-14 13:32:17.000000000 +00:00
type: post
parent_id: '0'
published: true
password: ''
status: publish
categories:
- djangode
tags:
- pyqt
- pyside
- python
- qt
meta:
  _edit_last: '364050'
  _wpas_done_twitter: '1'
author:
  login: andrewjw
  email: andrewjwilkinson@gmail.com
  display_name: Andrew Wilkinson
  first_name: Andrew
  last_name: Wilkinson
permalink: "/2011/03/14/deadlock-on-exit-with-pyside-and-qfilesystemwatcher/"
---
<a href="http://www.flickr.com/photos/bohman/210977249/"><img src="{{ site.baseurl }}/assets/210977249_da533e62a4_m.jpg" alt="Keys by bohman" style="float:right;border:0;" /></a>Last year Nokia started developing their own Python bindings for Qt, <a href="http://www.pyside.org">PySide</a>, when they couldn't persuade Riverbank Computing to relicense <a href="http://www.riverbankcomputing.co.uk/software/pyqt/intro">PyQt</a> under a more liberal license. While developing <a href="http://www.djangode.com">DjangoDE</a> I made the choice of which library to use configurable. When running under PyQt everything worked fine, but when using PySide the program hung on exit.n
Using gdb to see where it was hanging points to <a href="http://doc.qt.nokia.com/4.7/qfilesystemwatcher.html">QFileSystemWatcher</a>, which has the following comment in the destructor.n
<blockquote>
Note: To avoid deadlocks on shutdown, all instances of QFileSystemWatcher need to be destroyed before QCoreApplication. Note that passing QCoreApplication::instance() as the parent object when creating QFileSystemWatcher is not sufficient.
n</blockquote>
The following code will demonstrate the issue.n
[code lang="python"]<br />
import sysn
#from PyQt4 import QtGui<br />
from PySide import QtGuin
app = QtGui.QApplication(sys.argv)n
file_browser = QtGui.QTreeView()<br />
file_model = QtGui.QFileSystemModel()<br />
file_model.setRootPath(&quot;/&quot;)<br />
file_browser.setModel(file_model)n
file_browser.show()n
sys.exit(app.exec_())<br />
[/code]n
As the comment says, we need to ensure that the <tt>QFileSystemWatcher</tt> object, which is created by <tt>QFileSystemModel</tt>, is destroyed before <tt>QApplication</tt>. To do this we can connect to the <tt>lastWindowClosed</tt> and ensure that the <tt>QFileSystemModel</tt> is fully destroyed.n
[code lang="python"]<br />
import gcn
def app_quit():<br />
     global file_browser<br />
     file_browser = None<br />
     gc.collect()n
app.lastWindowClosed.connect(app_quit)<br />
[/code]n
It's not clear why this code would work on PyQt and not PySide, but it is clearly related to the order the objects are deleted. Given the comment in the Qt documentation though you should probably not rely on it working on PyQt and ensure yourself that the <tt>QApplication</tt> is the last Qt object to be destroyed.n
<hr />
Photo of <a href="http://www.flickr.com/photos/bohman/210977249//">Keys</a> by <a href="http://www.flickr.com/photos/bohman/">bohman</a>.n
