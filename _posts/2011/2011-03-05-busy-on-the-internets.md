---
title: Busy on the Internets
layout: post
date: 2011-03-05
---
I&rsquo;ve been busy around the Internets this week; most of this centres around collectd; monitoring tool extraordinaire.

  * I&rsquo;ve gotten to know [collectd][1]&lsquo;s very pleasant source code, and contributed some new functionality (which non-coincidentally work benefits from). You can use this to have threshold notifications constantly report their status (previously you could only configure collectd to constantly report failures and warnings, not &lsquo;okay&rsquo; messages). [Patches for &lsquo;master&rsquo; and 4.10.][2] (Or, if you use Ubuntu, keep reading).
  * If we&rsquo;re going to roll out collectd, then 95th percentile lines on the graphs are a must. [collectd-web][3] was the closest match to work&rsquo;s requirements, though in the end not an ideal fit. Either way, it&rsquo;s a good basis, so there&rsquo;s a 95th patch, as well as basic Varnish and Conntrack plugin definitions [on my fork][4].
  * The jQuery goodies in collectd-web aren&rsquo;t _really_ what I wanted from a web interface. I miss the old-time HTML-ness of [Munin][5], and have attempted to recreate some of that with my first [Flask][6] app, [collectd-flask][7]. No documentation is provided, if it did exist it would be likely to be longer than the source code.
  * Given that there&rsquo;s now functionality in patches for collectd that I need rolled out to a lot of machines, the obvious thing to do is build Debian packages. However, lacking any kind of private repository, using Ubuntu&rsquo;s (really excellent) [personal package archives][8] has been great. You just build a source package, use dftp to upload it and then a Xen instance somewhere in the cloud builds your package for you (or, not, depending on errors). There&rsquo;s now a [PPA for Lucid][9] with the [Varnish plugin][10] and PersistOK patch, and [for Maverick][9] with just PersistOK.
  * The Lucid package is maintained in [this Bazaar repo][11]. Previously it was maintained by running &ldquo;diff -ru&rdquo; a bunch of times. Memories.

Basically _all_ of the infrastructure to do this is available via hosted services, almost exclusively free. I developed the patches on an Ubuntu VM, though technically you can get one of those for [free from Amazon][12] for a year. If you were very confident or patient, you could actually develop with a compiler, using the PPA service as your build server. (Though, that&rsquo;s probably a pretty anti-social use of a shared resource).

Coding in the cloud; it&rsquo;s here, and I&rsquo;m late to it.

 [1]: http://collectd.org
 [2]: http://mailman.verplant.org/pipermail/collectd/2011-March/004383.html
 [3]: http://kenny.belitzky.com/projects/collectd-web
 [4]: https://github.com/insom/collectd-web
 [5]: http://munin-monitoring.org
 [6]: http://flask.pocoo.org/
 [7]: https://github.com/insom/collectd-flask
 [8]: https://help.launchpad.net/Packaging/PPA
 [9]: https://launchpad.net/~bradya/+archive/collectd/+packages
 [10]: http://collectd.org/wiki/index.php/Plugin:Varnish
 [11]: https://code.launchpad.net/~bradya/+junk/collectd-persistok-varnish
 [12]: http://aws.amazon.com/free/


