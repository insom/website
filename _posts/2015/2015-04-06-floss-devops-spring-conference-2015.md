---
title: FLOSS DevOps Spring Conference 2015
author: Aaron Brady
layout: post
date: 2015-04-06
url: /2015/04/floss-devops-spring-conference-2015/
categories:
  - Uncategorized
---
A couple of weeks ago some [of][1] [my][2] [colleagues][3] and [I][4] travelled to York for the FLOSS UK Spring Conference (now named DevOps Spring in some places, but not in others&hellip;), and in the spirit of blogging things, I thought I&rsquo;d write up the experience.

The Spring Conference was my first conference experience at [work][5] (in 2011) and is the first place I gave a [proper talk][6] (in 2013). It&rsquo;s also perfectly timed for us at work because it happens before April, when Ubuntu LTS releases come out. 

We use the LTS cycle to implement changes to our infrastructure, so new things that we learn at the conference can potentially be put to work right away and it gets the operations team out of the office and able to gather our thoughts for the next cycle.

We got our first taste of [Ansible][7] from [jpmens][8]&lsquo; talk in 2013, and that&rsquo;s transformed how we work, so it&rsquo;s been good value so far!

Anyway, that&rsquo;s the conference in general, but I&rsquo;m writing up this one specifically.

<blockquote class="twitter-tweet" lang="en">
  <p>
    Another lovely day in York! (just kidding, it&rsquo;s raining &mdash; this is from yesterday) <a
href="https://twitter.com/hashtag/flossuk2015?src=hash">#flossuk2015</a> <a
href="http://t.co/dGsJylSMVH">pic.twitter.com/dGsJylSMVH</a>
  </p>
  
  <p>
    &mdash; iWeb (@iwebtweets) <a
href="https://twitter.com/iwebtweets/status/581020766726017025">March 26, 2015</a>
  </p>
</blockquote>



York is a great location, it&rsquo;s central, pretty and on a major train line. The Hilton, where the conference was held, was great &mdash; although it has an amazingly expensive bar &mdash; and the facilities and catering were great.

Projection, which is fraught with problems at most community conferences, worked well and the whole conference was recorded by a professional AV crew (speakers wore lapel mics and everything!). I&rsquo;m keen to see the video that comes out of the conference this year.

That said, when the rooms were joined it would have been great to have amplification. [Staffs Web Meetup][9] has PA, and that&rsquo;s for a single room with about 50 attendees. Maybe I&rsquo;m spoiled, but it makes a big difference, and acknowledges that not everyone has perfect hearing.

### Sponsors {#sponsors}

Google, 2nd Quadrant, Eligo and O&rsquo;Reilly had stands set up with merchandise, prize draws and puzzles. There&rsquo;s a standing discount on O&rsquo;Reilly books for UKUUG members, so it&rsquo;s actually a great time to pick up a book, especially if a talk has ignited an interest in something new.

The Google draw was for a Chromebook, which none of us wanted enough to go out and buy, but were oddly drawn to when the chance to win one for free came up :). Like most Google presence at conferences, there are quick tests and puzzles and a form to fill in with recruiterish information (like what level of education you have, and what your GitHub account is).

{ Disclosure: I won a spot prize! I got 100% on the SRE test, which only me and [Stu Teasdale][10] managed. The SRE test was definitely easier than the software development one, though, or maybe that&rsquo;s my bias showing. }

<blockquote class="twitter-tweet" lang="en">
  <p>
    Woot I just won a bag for getting 100% on Google&rsquo;s test <a
href="https://twitter.com/hashtag/flossuk2015?src=hash">#flossuk2015</a> <a
href="http://t.co/xmFfmei2Cv">pic.twitter.com/xmFfmei2Cv</a>
  </p>
  
  <p>
    &mdash; Aaron Brady (@insom) <a
href="https://twitter.com/insom/status/580750271128715265">March 25, 2015</a>
  </p>
</blockquote>



### The Keynote {#the-keynote}

The &ldquo;keynote&rdquo; was by John Leach, who gave a great introduction to what Docker is, how it works and when to use it (and not use it). His presentation timing was great and the whole thing was pretty engaging. He kept questions to the end (good!) and, considering he was addressing a space the size of three rooms, was audible from the back.

Keynote is in scare quotes because I tend to think of keynotes at conferences as being general interest and largely non-technical &#8211; this was a good talk, but could have gone in any talk slot. PyCon UK, for example, uses these slots for invited guest speakers and things that affect the whole community.

I know that the original speaker for that slot pulled out at the last minute, for which affordances should be made, but the second day keynote by Stu Teasdale was similarly a technical talk suited to any slot.

### Talks {#talks}

I enjoyed the talks that I went to: Enhancing SSH for Security & Utility, Shipping your product with Puppet code, Open Source Monitoring with Icinga, Build Management with a dash of Prolog, Beyond Blue-Green, Introduction to Btrfs, and Kerberos &#8211; Protocol and Practice.

{ Here&rsquo;s the [Lanyrd page][11] if you&rsquo;d like more detail on any talk }

The speakers all did a good job and everyone was pretty good at keeping to their time. FLOSS is the kind of conference where attendees will just shout questions at you in the middle of your talk and I wish the session chairs would intervene when talks are being pulled off course: it&rsquo;s stressful enough presenting when you&rsquo;re just sticking to your prepared material and there is dedicated Q&A time, after all.

The lightning talks were also fun (more disclosure: [Ed][3] and I gave one each) though unusually stressful to present as seeing the presenter struggle to finish in their time-slot seems like part of it. I particularly found the `bash` shortcuts useful as they mostly work in `zsh` and, well, I use a shell every day.

<blockquote class="twitter-tweet" lang="en">
  <p>
    Lightning talk #2, this time from <a href="https://twitter.com/insom">@insom</a> <a
href="https://twitter.com/iwebtweets">@iwebtweets</a> <a
href="http://t.co/kJBL9k3wdq">pic.twitter.com/kJBL9k3wdq</a>
  </p>
  
  <p>
    &mdash; Neil Boughton (@NeilBoughton) <a
href="https://twitter.com/NeilBoughton/status/580773856509591552">March 25, 2015</a>
  </p>
</blockquote>



### Criticism {#criticism}

It&rsquo;s not easy to put on a conference, and I don&rsquo;t really have good suggestions for improving the following things, especially because my main issues are around the talks and people at the conference, which are just about the hardest things to change.

The second day was a lot _thinner_ than the first, it had fewer talks in general and they were less relevant to our industry than the first day. The conference actually ended up being wrapped ahead of schedule, and while that meant getting home earlier (yay) it does really mean if you excluded closing notes and the prize draw, it&rsquo;s really a one and a half day conference, not a two day one.

Also, despite rebranding as a &ldquo;DevOps&rdquo; conference, the material is largely the same as it has been every year that I&rsquo;ve gone: reasonably technical Unix material.

No one agrees on what DevOps is, but at other DevOps-themed conferences I&rsquo;ve seen a lot more focus on solving business problems and workflows which integrate developers. DevOps, IMHO, is not just throwing Puppet and Ansible at a problem.

Unless you count Perl, developers are heavily under-represented at the Spring conference. As are business people. I&rsquo;d actually consider the whole conference to be a bit anti-dev and anti-business, too, which is a little sad because it perpetuates the BOFH stereotype and cuts of avenues for growth.

The conference could be a one day event and have a better pace, but then people may not want to travel for a single day event &mdash; which could lead to a lower attendance and potentially even fewer talks.

Even if the organisers _did_ want to create a more inclusive DevOps event (for example: with devs), where would they find them? The pool that they&rsquo;re drawing from is largely organisations that are UK Unix User Group members, and that isn&rsquo;t growing.

[iWeb][5] is generous enough to send us to a conference (sometimes more than one) every year, but that means that we need to be choosy about where we go and it&rsquo;s getting harder to choose the Spring conference over other events.

 [1]: https://twitter.com/neilboughton
 [2]: https://twitter.com/dazworrall
 [3]: https://twitter.com/ejrowley
 [4]: https://twitter.com/insom
 [5]: http://www.iwebsolutions.co.uk/
 [6]: https://speakerdeck.com/insom/realtime-monitoring-at-scale
 [7]: http://ansible.cc/
 [8]: http://jpmens.net/
 [9]: http://staffswebmeetup.co.uk/
 [10]: https://twitter.com/bmoosefh
 [11]: http://lanyrd.com/2015/flossuk/


