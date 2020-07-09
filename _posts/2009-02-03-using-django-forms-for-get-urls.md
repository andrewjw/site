---
layout: post
title: Using Django Forms For GET Urls
date: 2009-02-03 13:25:04
type: post
categories:
- web development
tags:
- django
- forms
- tip
- web development
permalink: "/2009/02/03/using-django-forms-for-get-urls/"
---
A regular occurance in writing webapps is the user will submit a form, and on the results page you'll want to include a link which the user can click to resubmit the form. This lets users bookmark the page or you can add an extra parameter such as 'format' so they can download the results.</p>

While Django forms contain several functions for converting the form to HTML, it doesn't contain one to convert a bound form to url arguments.</p>

Fortunately Python's standard library module <tt>urllib</tt> contains a module which converts a dictionary to a properly formatted url argument string. We simply add a function, <tt>as_url_args</tt>, which passes the form's cleaned data to this function and we get back a nice string we can add to a link.</p>

    import urllib
    from django import forms
    
    class MyForm(forms.Form):
        name = forms.CharField
    
        def as_url_args(self):
            return urllib.urlencode(self.cleaned_data)    

To use this in a template, where <tt>form</tt> is the form object, we can add it to a link.</p>

    <a href="/form?{{ form.as_url_args }}&amp;format=csv">Download As CSV</a>
