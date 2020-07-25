+++
date = "2016-04-21T19:05:09Z"
title = "Giving up on Cachet, diving into CloudStack VXLANs"
type = "journal"
+++

I've officially [bowed out of adding multiple API keys to Cachet][bow]. It
feels bad, but it feels better than just continuing to leave an open PR
unworked on.

In other green square news, I have yet another [CloudStack issue opened][cs].
This one wasn't just my work, three of us at iWeb spend a full working day
trying to figure the problem out. It looks like another commenter on that
issue had the same problem and worked around it - but for at least a release
CloudStack hasn't been able to migrate virtual machines which use VXLANs.

This is actually only the bottom problem in a stack; we found this while
trying to replicate a different bug which may actually lie in the Linux kernel
(or our specific Linux networking configuration) - expect updates if we solve
*that* one.

It requires so much intense concentration to chase bugs like this and when you
come out the other side the sense of relief and achievement is amazing, but
every obscure bug like this leads to some soul searching: after seeing packets
arrive on a NIC and then disappear before hitting the right Linux bridge
device, we were questioning whether we just misunderstood some basic tcpdump
BPF syntax. You know, just a tool I've been using for 15 years.

[bow]: https://github.com/CachetHQ/Cachet/issues/496
[cs]: https://github.com/apache/cloudstack/pull/1513

