---
layout: post
title: Deriving From Untypable Classes
date: 2021-08-06
tags: python
permalink: "/2021/08/06/deriving-from-untypable-classes/"
flickr_user: 'https://www.flickr.com/photos/funkyah/'
flickr_username: Funkyah
flickr_image: 'https://live.staticflickr.com/3183/2615077817_fdd16ac319.jpg'
flickr_imagelink: 'https://www.flickr.com/photos/funkyah/2615077817/'
flickr_imagename: 'Funky Duck'
---
There's going to be a bit of a change of pace this week, compared to my more recent posts. This time we're
going to be getting deep into the weeds of Python typing.

One of the biggest recent changes to Python has been the introduction of type annotations. Back in the dim and
distant past I did my third-year university project on type inference in Python, around the time of Python
2.3. Now though, it's a much more mainstream part of the Python ecosystem. Alongside tools like
[black](https://black.readthedocs.io/en/stable/) and [pylint](http://pylint.pycqa.org/en/latest/), the type
checker [mypy](https://mypy.readthedocs.io/en/stable/) is a core part of my standard Python set-up.

Adding type annotations to your code, and integrating a type checker into your CI pipeline gives you many
of the benefits of a statically typed language, while retaining most the speed of development that
is associated with Python. The dynamic nature of Python, and the fact that type annotations haven't been widely
adopted by libraries that you might depend on, means that type checking has its limitations and sadly this means
it might not be obvious when the type checker has exceeded its abilities to detect errors.

Recently I was investigating a CI pipeline failure for a merge request opened by
[Renovate](https://github.com/renovatebot/renovate) for
[Google's BigQuery Python API library](https://github.com/googleapis/python-bigquery). The failure
was in `pylint`, saying that a type didn't have the attribute name we were using. At first, this seemed
like a simple failure, but after more investigation, I noticed something odd about it.
<!--more-->

```text
bin/filename.py:86:38: E1101: Instance of 'LoadJob' has no 'num_dml_affected_rows' member (no-member)
```

The code it was flagging the error for looked similar to the code below. The error was on the second line,
where the result of the query is being used.

```python
query = client.query(sql)
rows = query.num_dml_rows_affected
```

Why is the error being flagged for `LoadJob`? We're running a query, so wouldn't that be a `QueryJob`?
Checking the library documentation showed that `num_dml_rows_affected` was still a valid attribute, so the
error being raised is spurious. Checking the changes in the upgrade lead me to this
[pull request](https://github.com/googleapis/python-bigquery/pull/751). The pull request changes the `query`
function logic from:

```python
def run_query(job_id: int, sql: str) -> QueryJob:
    *snipped*

def query(sql: str) -> QueryJob:
    job_id = get_job_id()
    job = run_query(job_id, sql)
    return job
```

to:

```python
def run_query(job_id: int, sql: str) -> QueryJob
    *snipped*

def get_job(job_id: int) -> Union[QueryJob, LoadJob, ExtractJob]:
    *snipped*

def query(sql: str) -> QueryJob
    job_id = get_job_id()
    try:
        job = run_query(job_id, sql)
    except BigQueryError:
        job = get_job(job_id)
    return job
```

The new function call `get_job` returns a union of all of the different job types, but the original `query`
function only returns a `QueryJob`. Because the job id refers to the query we're executing `get_job` can only
ever return a `QueryJob`, but there's no way for any static analyser to know that. `pylint` relies on type
inference, and as far as I know doesn't use the type annotations to calculate return types. `pylint` infers
that the return type of `query` is now `Union[QueryJob, LoadJob, ExtractJob]`, when you try and use the return
value it will only succeed if the attribute is available on all possible types in the union. This explains
why the error was saying that `num_dml_rows_affected` is not available on a `LoadJob` object - it's not!

The `python-cloud-bigquery` project uses the `pytypes` type checker, but I confirmed `mypy` has the same
behaviour. The change to the library itself doesn't trigger any errors. It's only when using `pylint` on a call to the
library that an error is raised.

But why do the type checkers not flag this as a problem? Even if you know this code is correct there is no way
they can, and this is precisely the sort of error you use a type checker to try and prevent. There's something
fishy going on, so I tried to reproduce the error using as little code as I could.

```python
from typing import Optional, Union

class A:
    pass

class B(A):
    pass

class C(A):
    pass

def subfunc(arg: Optional[str]) -> Union[B, C]:
    if arg is None:
        return B()
    else:
        return C()

def func() -> B:
    r = B()
    r = subfunc(None)
    return r
```

Here we have three classes, the base class `A` and two derived classes. In `func` we have the variable `r`
which holds a `B`. We call `subfunc` which can return either `B` or `C`, and assign that to `r` before
returning it. Both `mypy` and `pytypes` flag `func` as having problems - it returns `Union[B, C]`, not the
`B` that was declared.

On further investigation, I discovered that my example code doesn't quite reflect what's going on in the
library. `A` is not the base class, it derives from a class from another library. Replacing `A` with
this next snippet of code is more accurate.

```python
import google.api_core.future.polling # type: ignore

class A(google.api_core.future.polling.PollingFuture):
    pass
```

Making this change causes the errors raised by both `mypy` and `pytypes` to disappear. They claim the
code is fine when clearly it's not. The `# type: ignore` part of the line is the smoking gun here.
It's needed for `mypy` (and inferred in `pytypes`) because Google's `api_core` library has not yet
added type annotations. All classes in this library get treated as the `Any` type, which means the
type check will essentially ignore any expression involving that type. This is normal and what I
would expect.

What I wasn't expecting was how this interacts with class hierarchies. When you derive from an
untyped class the derived class also becomes equivalent to the `Any` type (because the base
class is assumed to have all attributes), so all derived types are equivalent, in this case, `B`
and `C`. This in turn means that no errors are raised when returning `Union[B, C]` instead of `B`.

`pylint` picks this error up as (as far as I know) it doesn't yet take into account the type
annotations and is still relying on pure type inference. While the code in question is bug-free,
the automated checks are not able to help in verifying this. When the `api_core` library is updated with type annotations the
type checkers will start raising this error, despite the change to upgrade the library appearing to be unrelated.

The `Any` type has a very specific use in Python - when you are using the dynamic nature of Python
to go beyond what can be represented by the type system. This is something you should be careful
about and go into with your eyes open. What this discovery has taught me is that your
dependencies might also introduce the `Any` type into your code, and its effects can filter
through in some unexpected ways.

What do you think of type checking in Python? Have you found any edge cases? Let me know in the
comments below!
