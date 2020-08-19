---
layout: post
title: Dynamic Initial Values in Django Forms
date: 2009-01-28 13:33:14
tags:
- django
- forms
- web development
permalink: "/2009/01/28/dynamic-initial-values-in-django-forms/"
---
I recently had cause to create a form with two date time fields which had the default values of midnight seven days ago, and midnight this morning. Initially I thought this would be easy and created the following form.

    from datetime import datetime, date, timedelta
    
    class MyForm(forms.Form):
        date_from = forms.DateTimeField(label="From",
                                   initial=(date.today() - timedelta(days=7)))
        date_to = forms.DateTimeField(label="To", initial=date.today())

This works fine except that when a process has been running across more than one day the initial values are no longer correct as they refer to the day the process started. Fortunately it appears that there is an undocumented feature where the initial value can be a function rather than an absolute value. This function is called each time the unbound form is displayed, so they are always correct.

Wrapping the code to create the value in a `lambda` works great here, as does passing a reference to a function.

    from datetime import datetime, date, timedelta

    class MyForm(forms.Form):
        date_from = forms.DateTimeField(label="From",
                     initial=lambda: (date.today() - timedelta(days=7)))
        date_to = forms.DateTimeField(label="To", initial=date.today)
