---
title: 'Re: Is it right to seek out GPL code for free?'
author: Aaron Brady
layout: post
date: 2015-08-15
url: /2015/08/re-is-it-right-to-seek-out-gpl-code-for-free/
categories:
  - Uncategorized
---
> In this instance, I can’t be sure how much time was actually saved by making use of the extension. But it illustrates the ethical question I’m interested in. If you’re potentially going to save many hours of research/development, is it right to seek out the source code for free? 

(and also)

> And for me, I think this is where context is important. There is a difference between someone throwing their code up on GitHub for the world to see and a business selling access and support. 

The GPL encompasses an ideology as much as it is a license. Originally meant for things which were [being assigned to the FSF anyway][1], it has some provisions beyond the &#8220;share a-like&#8221; clauses which show it&#8217;s heritage- like the ability to upgrade to future, unwritten, versions of the GPL. [Some people don&#8217;t like this][2]. (There are people who don&#8217;t like the GPL for lots of reasons, some of which I agree with, some I don&#8217;t, and some I am pragmatic about).

The GPL is about freedom. If you&#8217;ve seen Dr. Stallman talk (and I have) he has some very harsh words to share about the phrase &#8220;open source&#8221;. It&#8217;s not (just) about access to the source code &#8211; its about being able to do what you want with it, and with _your_ computing, as long as you don&#8217;t impinge on other people&#8217;s freedom to do the same.

I realise that Phil is posing an ethical question and not a legal one: shouldn&#8217;t you pay for software that saves you hours of work? It seems simple: &#8220;yes&#8221;. Or: &#8220;yes, but &hellip;&#8221;.

If you&#8217;re writing your code in Atom (open source editor, running on the open source Node runtime), to run under PHP (open source runtime), executing it all on a Linux kernel (GPLed) which was part of a Debian distribution (open source project _made up of_ even more open source projects) &#8211; why do you just pay the people who add that little bit of value-add on top? You owe a great debt to a lot of people.

The open source community at large relies on a, sometimes frustrating, set of different models for sustainability:

  * Some authors are employed to work on open projects (Redis, Python).
  * Some companies offer their product under open licensning terms to encourage use and to sell professional services on top (MongoDB, MySQL).
  * Some people try and sell their open software and hope people don&#8217;t redistribute it (WooCommerce).
  * Some dual license, well aware of what a poison pill the GPL is to many businesses (MySQL Again).
  * Lots of projects receive no formal funding and run on volunteer effort &#8211; volunteers enjoy the satisfaction of a job well done, or the admiration of their peers, or the benefits that a CV filled with open contributions gives when looking for employment.

Sometimes, when a project is instrumental to someone&#8217;s success, [they make a large donation to a foundation][3], recognising that fact (FreeBSD/WhatsApp).

[Patrick McKenzie has written about how frustrating most open source models are][4] when you&#8217;re trying to run a company ethically &#8211; because really most companies _can&#8217;t_ be ethical.

For the most part (and in some places in the world this is a legal requirement) &#8211; companies run to maximise the profits for their owners. If you offer software for free but solicit a donation for use, it&#8217;s unlikely a company can easily comply with that (unless you&#8217;re a registered charity, and even then it&#8217;s a lot of hassle). If you _sell_ your product, it&#8217;s a little easier, but if a company is aware it can receive an _identical_ product for free, its employees would be acting against its shareholders&#8217; interests if they paid for it.

Patrick certainly seems to come down on the side of offering enterprise support as a sustainable model. Something you _can&#8217;t_ get for free, something which the solicitors and legal and finacial people in a company can understand (buying indemnity).

Companies can&#8217;t be expected to act ethically, even though individuals can, but people hoping to make a living out of open source software need to adopt business models not based on pity. If you license your software as GPL but expect to keep the source closed, you are fooling yourself and relying on people _not_ exercising their rights.

 [1]: https://en.wikipedia.org/wiki/GNU_General_Public_License#History
 [2]: http://www.informationweek.com/the-torvalds-transcript-why-i-absolutely-love-gpl-version-2/d/d-id/1053128
 [3]: http://freebsdfoundation.blogspot.co.uk/2014/11/freebsd-foundation-announces-generous.html
 [4]: http://www.kalzumeus.com/2014/04/03/fantasy-tarsnap/




