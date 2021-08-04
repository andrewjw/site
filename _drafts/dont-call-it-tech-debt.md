---
title: Don't Call It Tech Debt
---
A common refrain from developers is "We have too much tech debt! We need to tackle it to
speed up!" It's hard to argue with the sentiment - badly written code or outdated software does
take considerably more effort to maintain than code that follows best practices. However, saying
we have too much tech debt is not useful, because it's not specific enough. You can't create a
"tackle tech debt" project and expect to get sponsorship from the business for the work.

If you're lucky enough to have a portion of your time available to be used for engineering
directed projects then you're still unlikely to be successful with a tech debt project
because getting agreement for what actually is tech debt is nigh-on impossible. Everyone
has their own pet peeve that they will want to tackle as part of that project.

My solution to this problem is to avoid using the word tech debt. Sometimes tech debt is clear -
it might be a database that is outside of its support lifecycle or a library that is many versions
behind the current release. More common is that when people say "tech debt" they mean things like
code that is not as testable as they would like, or which follows some patterns that they declare
to be an anti-pattern. While there is broad agreement about what constitutes good code, the more
detailed you get the more it becomes about personal opinions.

The key to a good technical project is the same as with a good business-driven project - you need
clear aims, a well-defined definition of done and a coherent set of steps to get you there. Let's
look at the three types of technical projects outlined above.

The simplest case is upgrading an outdated database or library. Getting alignment on the goals of
the project can be achieved by creating a policy around the supported version. Perhaps you want to always
be running the n-1 major release version, or treat anything that has a new version released more
than two weeks ago as outdated. Whatever rule you decide on it's relatively easy to apply the rule
across your codebase (particularly if you use something like
[Renovate](https://www.whitesourcesoftware.com/free-developer-tools/renovate/)) and come up with a
well-defined project to address that debt.

Let's now consider the case where people say that code is as not as easy to test as it should be.
This is much harder to define a rule for, compared to outdated versions. What you can do though it
defined coding standards to enforce testability. Perhaps you always want to use dependency
injection to make it easy to mock dependencies out. Maybe instead you're worried about your
tests being too high-level and therefore too fragile. Your coding standard should define acceptable
patterns which can then be compared to your code to provide a list of targets for refactoring.
Providing your obtained enough buy in and agreement when defining the standards there should be
little argument about what code to tackle. This is likely to highlight a large number of targets
so prioritising based on a measure of flakiness is probably worthwhile.

The final case I want to consider is the more general case where people suggest that your code
contains "anti-patterns" that need to be refactored. 


