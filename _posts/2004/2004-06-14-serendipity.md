---
title: Serendipity and the 301 HTTP status code.
date: 2004-06-14
---

I had just finished reading Sam Ruby's ["Gone, really I mean it"][gone] post,
and decided to use "301 Permanently Moved" HTTP codes for my feed redirects.

[gone]: http://www.intertwingly.net/blog/2004/06/13/Gone-Really-I-mean-it

I noticed Planet Python in my access log around this time and
went to look it up and check that, even though they are all valid, my feeds
actually work.

In the long list of people at the top of the page, it has a link to my RSS 2.0
feed. What is the link URI? `http://insom.me.uk/blog/rss20`! In less than 10
minutes, it has updated itself to using the _correct_ address. This
shouldn't be surprising; it's what 301 means, but it was still very cool.
