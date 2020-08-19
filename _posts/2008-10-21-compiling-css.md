---
layout: post
title: Compiling CSS
date: 2008-10-21 12:30:35
type: post
tags: css web
permalink: "/2008/10/21/compiling-css/"
---
A new compiler called [HSS](http://ncannasse.fr/projects/hss) has been released. This tool makes it
easier to write concise, maintainable and valid CSS. The two key features are the ability to define variables
which are then replaced throughout the file, and to create nested blocks.

Typically you'll need to write code like this:

    .faq {
        color: red;
    }
    .faq h1 {
        background-color: black;
    }
    .faq a {
        text-decoration: none;
    }

With HSS you can write...

    .faq {
        color: red;
        h1 { background-color: black; }
        a { text-decoration: none; }
    }

Since you'll want to automatically run a code minimiser over your CSS code anyway, running HSS as well shouldn't be a problem.

Unfortunately the tool is written in the little known language [Neko](http://nekovm.org/) (which is a language
created by the author of HSS) and is not hosted on any of the of many open source project hosting sites which would help
ensure the tool lives on even if the author moves on. Indeed, it's not even clear from the website what license the tool
is released on. These are problems that might need to be solved before it's worth basing a project around HSS.

