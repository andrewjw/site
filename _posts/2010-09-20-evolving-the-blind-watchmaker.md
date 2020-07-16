---
layout: post
title: Evolving The Blind Watchmaker
date: 2010-09-20 12:00:30.000000000 +01:00
type: post
parent_id: '0'
published: true
password: ''
status: publish
categories:
- python
tags:
- evolution
- genetics
- programming
- richarddawkins
- trees
meta:
  _edit_last: '364050'
  _wp_old_slug: ''
  _wpas_done_twitter: '1'
author:
  login: andrewjw
  email: andrewjwilkinson@gmail.com
  display_name: Andrew Wilkinson
  first_name: Andrew
  last_name: Wilkinson
permalink: "/2010/09/20/evolving-the-blind-watchmaker/"
---
<a href="http://www.flickr.com/photos/joiseyshowaa/1400175456/"><img src="{{ site.baseurl }}/assets/1400175456_f5bcfb085d_m_d.jpg" alt="my tree at dusk by joiseyshowaa" style="float:right;border:0;" /></a>Recently I've been reading the classic book by <a href="http://www.richarddawkins.net/">Richard Dawkins</a>, <a href="http://books.google.com/books?id=zHc9PgAACAAJ&amp;dq=blind+watchmaker">The Blind Watchmaker</a>. In it he begins by discussing how evolution can produce complex systems from only a few simple rules. He demonstrates this using a simple tree drawing algorithm in which a few 'genes' control aspects such as the number of branches and the branch angle. The trees are evolved solely through mutation of an initial tree, rather combing the 'genes' of two trees to produce a child, and introducing mutations in those children.n
In reality evolution is driven by pressures from the environment on the genes and those that produce the fittest host will survive. As this is early in the book though Dawkins uses himself as the environment and manually picks the most visually appealing trees.n
Although the book is essentially timeless as although new evidence is continually being found in favour of evolution, the general thrust remains true. The passages where he talks about his computer, however, have dated horribly (which is not surprising given it was first published in 1986!). In this post I'll describe how to recreate the section where he describes evolving trees in Python so you can create your own trees on your pc.n
As with the book our trees will be controlled by nine genes, each of which is an integer. Dawkins doesn't state what the nine genes do as for his purposes that would confuse matters, but for us it's vital. Fortunately figure three allows us to work out what genes one, five, seven and nine do for ourselvesn
<ol>
<li><b>Horizontal scaling</b></li>
<li>Number of branches per level</li>
<li>Length of first branch</li>
<li>Scaling factor for length of subsequent branches</li>
<li><b>Vertical scaling</b></li>
<li>Angle of first branch</li>
<li><b>Angle of branching</b></li>
<li>Scaling factor for angle of branching</li>
<li><b>Levels of branching</b></li>
</ol>
The gene descriptions in bold are those that I deduced from the book, the others are ones I decided on myself. The first step in writing a program like this is to decide exactly how these genes will affect the drawn tree. To do this we create a series of functions, one for each gene, that converts the gene value into a value that can be used by the drawing code. These functions are given below.n
[sourcecode language="python"]<br />
horiz_scaling = lambda dna: (dna[0]+10.0)/10.0<br />
branches = lambda dna: dna[1]<br />
initial_length = lambda dna: dna[2] + 10<br />
length_scaling = lambda dna: (dna[3]+10.0)/10.0<br />
vert_scaling = lambda dna: (dna[4]+10.0)/10.0<br />
initial_angle = lambda dna: dna[5]/10.0<br />
initial_angle_of_branching = lambda dna: 1.0+dna[6]/5.0<br />
change_in_angle_between_branches = lambda dna: dna[7]/5.0<br />
max_levels = lambda dna: dna[8]<br />
[/sourcecode]n
These functions are used by the <tt>draw_branch</tt> function which renders a single line, and recursively calls itself to draw the next level of branches.n
[sourcecode language="python"]<br />
def draw_branch(img, dna, level, start, angle, length, angle_between_all_branches):<br />
    end = (start[0] + math.sin(angle) * length * horiz_scaling(dna),<br />
              start[1] - math.cos(angle) * length * vert_scaling(dna))<br />
    img.line(start + end, (0, 0, 0))n
    if level &gt;= max_levels(dna):<br />
        return<br />
    else:<br />
        branch_angle = angle - angle_between_all_branches/2.0<br />
        angle_between_branches =<br />
            0 if branches(dna) == 0 else angle_between_all_branches/branches(dna)<br />
        for i in range(branches(dna)+1):<br />
            draw_branch(img, dna, level+1, end,<br />
                branch_angle + angle_between_branches*i, length*length_scaling(dna),<br />
                angle_between_all_branches + change_in_angle_between_branches(dna))<br />
[/sourcecode]n
To start the drawing process off we need a function, <tt>draw_tree</tt>, which calls the branch drawing function with the initial values for the length of branch and angle between the subbranches.n
[sourcecode language="python"]<br />
def draw_tree(img, dna):<br />
    draw_branch(img, dna, 0, (50, 70),<br />
        initial_angle(dna), initial_length(dna), initial_angle_of_branching(dna))<br />
[/sourcecode]n
Now we can draw a tree a we need to be able to generate the children of tree, which we do by picking a gene and either incrementing or decrementing it. A couple of genes make no sense if they are negative so they code prevents these from going below zero.n
[sourcecode language="python"]<br />
def evolve(dna):<br />
    gene = random.choice(range(9))n
    if (gene in [1, 8] and dna[gene] == 0) or random.random() &lt; 0.5:<br />
        dna[gene] += 1<br />
    else:<br />
        dna[gene] -= 1n
    return dna<br />
[/sourcecode]n
If we combine these functions with a simple TK-based interface, as shown below, we exactly the abilities described in The Blind Watchmaker book. Nine possible trees are displayed, when the user clicks on one nine new children are created and displayed.n
<a href="http://andrewwilkinson.files.wordpress.com/2010/09/trees1.png"><img src="{{ site.baseurl }}/assets/trees1.png" alt="" title="Dawkin's Trees" width="326" height="345" class="alignleft size-full wp-image-279" /></a>n
<a href="http://andrewwilkinson.files.wordpress.com/2010/09/trees2.png"><img src="{{ site.baseurl }}/assets/trees2.png" alt="" title="Dawkin's Trees" width="326" height="345" class="alignleft size-full wp-image-279" /></a>n
Without more details about the original program it's hard to recreate it exactly, but this program is a decent starting point. Happy evolving!n
To run this program yourself you'll need to download and install Python from <a href="http://www.python.org">python.org</a> and the <a href="http://www.pythonware.com/products/pil/">PIL image library</a>. Next code the sourcecode below into a file called "darwkins_trees.py" and double click on it.n
[sourcecode language="python"]<br />
#!/usr/bin/env pythonn
# Copyright &lt;year&gt; &lt;copyright holder&gt;. All rights reserved.<br />
#<br />
# Redistribution and use in source and binary forms, with or without modification, are<br />
# permitted provided that the following conditions are met:<br />
#<br />
#   1. Redistributions of source code must retain the above copyright notice, this list of<br />
#      conditions and the following disclaimer.<br />
#<br />
#   2. Redistributions in binary form must reproduce the above copyright notice, this list<br />
#      of conditions and the following disclaimer in the documentation and/or other materials<br />
#      provided with the distribution.<br />
#<br />
# THIS SOFTWARE IS PROVIDED BY &lt;COPYRIGHT HOLDER&gt; ``AS IS'' AND ANY EXPRESS OR IMPLIED<br />
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND<br />
# FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL &lt;COPYRIGHT HOLDER&gt; OR<br />
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR<br />
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR<br />
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON<br />
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING<br />
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF<br />
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.<br />
#<br />
# The views and conclusions contained in the software and documentation are those of the<br />
# authors and should not be interpreted as representing official policies, either expressed<br />
# or implied, of Andrew Wilkinson.n
import math, os, random, sys<br />
from Tkinter import *<br />
import Image, ImageTk, ImageDrawn
image_size = (100, 100)<br />
samples = 9n
horiz_scaling = lambda dna: (dna[0]+10.0)/10.0<br />
branches = lambda dna: dna[1]<br />
initial_length = lambda dna: dna[2] + 10<br />
length_scaling = lambda dna: (dna[3]+10.0)/10.0<br />
vert_scaling = lambda dna: (dna[4]+10.0)/10.0<br />
initial_angle = lambda dna: dna[5]/10.0<br />
initial_angle_of_branching = lambda dna: 1.0+dna[6]/5.0<br />
change_in_angle_between_branches = lambda dna: dna[7]/5.0<br />
max_levels = lambda dna: dna[8]n
def draw_branch(img, dna, level, start, angle, length, angle_between_all_branches):<br />
    end = (start[0] + math.sin(angle) * length * horiz_scaling(dna), start[1] - math.cos(angle) * length * vert_scaling(dna))<br />
    img.line(start + end, (0, 0, 0))n
    if level &gt;= max_levels(dna):<br />
        return<br />
    else:<br />
        branch_angle = angle - angle_between_all_branches/2.0<br />
        angle_between_branches = 0 if branches(dna) == 0 else angle_between_all_branches/branches(dna)<br />
        for i in range(branches(dna)+1):<br />
            draw_branch(img, dna, level+1, end, branch_angle + angle_between_branches*i, length*length_scaling(dna), angle_between_all_branches + change_in_angle_between_branches(dna))n
def draw_tree(img, dna):<br />
    draw_branch(img, dna, 0, (50, 70), initial_angle(dna), initial_length(dna), initial_angle_of_branching(dna))n
def evolve(dna):<br />
    gene = random.choice(range(9))n
    if (gene in [1, 8] and dna[gene] == 0) or random.random() &lt; 0.5:<br />
        dna[gene] += 1<br />
    else:<br />
        dna[gene] -= 1n
    return dnan
class Application(Frame):<br />
    def __init__(self, master=None):<br />
        Frame.__init__(self, master)n
        self.dna = [0, 1, 0, 0, 0, 0, 0, 0, 1]n
        self.grid()<br />
        self.create_widgets()n
        self.create_choices()n
    def create_widgets(self):<br />
        self.buttons = []<br />
        for i in range(samples):<br />
            button = Button(self)<br />
            button[&quot;command&quot;] = self.choose_tree(i)n
            button.grid(row=i / 3, column=i % 3)n
            self.buttons.append(button)n
    def create_choices(self):<br />
        self.choices = [evolve(self.dna[:]) for i in range(samples)]n
        self.images = [Image.new(&quot;RGB&quot;, image_size, (255, 255, 255)) for _ in range(samples)]<br />
        [draw_tree(ImageDraw.Draw(self.images[i]), self.choices[i]) for i in range(samples)]<br />
        self.tkimages = [ImageTk.PhotoImage(image) for image in self.images]n
        for i in range(samples):<br />
            self.buttons[i][&quot;image&quot;] = self.tkimages[i]n
    def choose_tree(self, i):<br />
        def func():<br />
            self.dna = self.choices[i]n
            self.create_choices()<br />
        return funcn
if __name__ == &quot;__main__&quot;:<br />
    root = Tk()<br />
    app = Application(master=root)<br />
    app.mainloop()<br />
    root.destroy()<br />
[/sourcecode]n
<hr />
Photo of <a href="http://www.flickr.com/photos/joiseyshowaa/1400175456">my tree at dusk</a> by <a href="http://www.flickr.com/photos/joiseyshowaa">joiseyshowaa</a>.n
