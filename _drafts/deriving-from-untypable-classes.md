---
layout: _post
title: Deriving From Untypable Classes
date: 2021-07-30
tags: python
permalink: "/2021/07/30/deriving-from-untypable-classes/"
---
There's going to be a bit of a change of pace this week, compared to my more recent posts. This time we're
going to be getting deep into the weeds of Python typing.

One of the biggest recent changes to Python has been the introduction of type annotations. Back in the dim and
distant past I did my third year university project on type inference in Python, around the time of Python
2.3. Now though, it's a much more mainstream part of the Python ecosystem. Alongside tools like
[black](https://black.readthedocs.io/en/stable/), [pylint](http://pylint.pycqa.org/en/latest/) the type
checker [mypy](https://mypy.readthedocs.io/en/stable/) is a core part of my standard Python set up.

Adding type annotations to your code, and integrating a type checker into your CI pipeline gives you many
of the benefits of a statically type language, while retaining most the speed of development that
associate with Python. The dynamic nature of Python, and the fact that type annotations haven't been widely
adopted by libraries that you might depend on, means that type checking has its limitations and it might not
be obvious when it your code has exceeded its abilities to detect errors.

Recently I was investigating a CI pipeline failure for a merge request opened by Renovate for Google's
BigQuery Python API library. The failure was in pylint, saying that a type didn't have the attribute name
we were using. At first this seemed like a simple failure, but after more investigation I noticed something
odd about it.

```text
PyLint error message.
```

The code it was flagging the error for looked similar to the code below. The error was on the second line,
where the result of the query is being used.

```python
query = client.query(sql)
rows = query.num_dml_rows_affected
```

Why is the error being flagged for `LoadJob`? We're running a query, so wouldn't that be a `QueryJob`?
Checking the library documentation showed that `num_dml_rows_affected` was still a valid attribute, so the
error being raised is suprious. Checking the changes in the upgrade lead me to this
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

The new function call `get_job` returns a union of all different job types there are, but the original `query`
function only returns a `QueryJob`. Because the job id refers to the query we're executing `get_job` can only
ever return a `QueryJob`, but there's no way for any static analyser to know that. `pylint` relies on type
inference, and as far as I know doesn't use the type annotations to calculate return types. `pylint` infers
that the return type of `query` is now `Union[QueryJob, LoadJob, ExtractJob]`, when you try and use the return
value it will only succeed if the attribute is available on all possible types in the union. This explains
why the error was saying that `num_dml_rows_affected` is not available on a `LoadJob` object - it's not!

The `python-cloud-bigquery` project use the `pytypes` type checker, but I confirmed `mypy` has the same
behaviour. The change to library doesn't trigger any errors. It's only when using `pylint` on a call to the
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
returning it. Both `mypy` and `pytypes` flag `func` has having problems - it returns `Union[B, C]`, not the
`B` that was declared.

On further investigation I discovered that my example code doesn't quite reflect what's going on in the
library. `A` is not actually the base class, it derives from a class from another library. Replacing `A` with
this next snippet of code is more accurate.

```python
import google.api_core.future.polling # type: ignore

class A(google.api_core.future.polling.PollingFuture):
    pass
```

Making this change causes the errors raised by both `mypy` and `pytypes` to disappear. They claim the
code is fine.
