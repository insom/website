---
title: Hating on git-submodule
author: Aaron Brady
layout: post
date: 2015-06-28
url: /2015/06/hating-on-git-submodule/
categories:
  - Uncategorized
---
<blockquote class="twitter-tweet" lang="en">
  <p lang="en" dir="ltr">
    <a href="https://twitter.com/DivineOmega">@DivineOmega</a> every time someone uses a submodule a puppy has a tree conflict.
  </p>
  
  <p>
    &mdash; Aaron Brady (@insom) <a href="https://twitter.com/insom/status/613412059691241472">June 23, 2015</a>
  </p>
</blockquote>



I feel that I should explain and defend my stance on git submodules. There are no doubt times when splitting a module into parts, or using submodules to import vendored dependencies is convenient. If this all works for you, that&#8217;s cool too.

For only referencing publicly available repositories that don&#8217;t change often _and_ that you don&#8217;t actively work on, I think it&#8217;s possibly even a _nice_ work flow.

Some of the drawbacks that I&#8217;ve experienced with submodules:

### Modifying files within a submodule

It&#8217;s easy to make changes in a submodule, commit and push and _think_ that everyone else has your change. Depending on where you have pushed they may _either_ have a new committish recorded in .gitmodules that they can&#8217;t reach _or_ you&#8217;ve pushed to a library&#8217;s repository and not updated the committish, so you&#8217;re puzzled why they don&#8217;t see your changes.

Updating the code in a submodule and making that visible to everyone requires two commits and two pushes. Depending on your continuous integration flow, that might also trigger two sets of tests.

### Dangling references in .gitmodule

I&#8217;ve experienced a developer pushing the top-level repository and then going on holiday, with the updated code for the submodule only existing on their laptop and them out of communication.

This leaves all of the downstream users unable to do a `git submodule update` until the .gitmodules file is manually updated to a previous version (and the work that relies on the module reverted or moved to a branch).

Yes, this is human error, but it&#8217;s both easier to do and more painful to fix than the alternatives.

### Merge ordering matters

If you push your outer project before any changed submodules, you may find that when you go to push the submodules you&#8217;ll need to merge or rebase because someone else has been working on it. Until you merge/rebase and push the submodule _and_ update the reference in your outer project _and_ commit and push, your project is in an unbuildable state.

### Relying on a single git URL

A git submodule encodes the git URL into the repository and repository history. Working at an organisation with over 1,000 git repositories, most of them private, we prefer to keep our git server private.

For situations where customers are working on code too, we mirror the source code or move it to a third-party, like a GitHub private repository.

Using submodules means either giving access to a third party to our git server (unacceptable) or duplicating the code in a place that they can access (expensive, with private GitHub repositories).

To make things worse, we foolishly renamed our git server a few years ago and _still_ find references to the old name, which require a git commit to change. Checking out old versions of our source which reference the old names always requires a manual step to get them working.

### Solving these problems

[git subtree is a fix for basically all of these problems][1]. It does feel like you&#8217;re using some dangerous git magic, and it&#8217;s definitely possible to get things wrong, but by and large you can carrying on working on a repository containing a subtree as if it was just one big repository.

Sharing with a customer means only exporting one git URL for them, and not hard-coding any URLs which may change into the history of the project.

Another approach that we&#8217;ve used, which does have some of the downsides of git submodules, is using the language vendor&#8217;s own packaging to ship our libraries, such as wrapping them in `pip install`able Python Eggs or Composer repositories. That&#8217;s bringing in more tools to learn, though, so you YMMV if you&#8217;re not already using those.

Thank you for reading. I feel much better.

 [1]: https://blogs.atlassian.com/2013/05/alternatives-to-git-submodule-git-subtree/


