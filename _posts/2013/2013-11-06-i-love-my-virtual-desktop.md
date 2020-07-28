---
title: I Love My Virtual Desktop
layout: post
date: 2013-11-06
---
![My Virtual Desktop][1]

I use a MacBook Pro at work, and a variety of Windowses at home, but the majority of my personal programming and hackery happens on a couple of machines called `Play` and `Beta`.

Play is an LXC container running on my [HP Microserver][3], and Beta is a KVM virtual machine running somewhere on the [iWeb Private Cloud][4] in Manchester.

Beta does the real work: [qpsmtpd][5], Exim and Dovecot to handle my mail, Apache for this blog, and any other long running daemons that I could consider &ldquo;production&rdquo; (as production as things get when you&rsquo;re doing this for yourself; typically meaning something my brother or wife will miss if it breaks).

Play has the checkouts of my personal git projects, my virtualenvs, vimrc, Git Annex: all that jazz. It&rsquo;s a well appointed Debian Jessie install with all the packages to make local development comfortable.

In a way, it&rsquo;s my &lsquo;ghetto&rsquo; box- all of my other containers and machines are minimal, only running daemons they need to do their jobs, and with spartan vi and bash configurations. If anything doesn&rsquo;t fit into the roles my other boxes are defined for, it goes on Play.

Because terminal emulators are a mixed bunch, and I&rsquo;m particular about everything from font, to keybindings to colour scheme, I run [vncserver][6] on Play with a light window manager ([mwm][7], because I&rsquo;m old school), and it guarantees that I can connect to the same session from work or home, and pick up exactly where I left off.

Play runs [BitTorrent Sync][8], now that I&rsquo;ve moved away from Dropbox, so I can have the same files accessible for anywhere, and move files in and out of my synced folders if I need to transfer things between devices. I even have Sync running on my phone, so I can get my photos off easily.

It means I can use my old Windows XP machine (which has some limited life left in it) to do real work, by basically using it as a full screen wireless VNC viewer (which, by the way, is a gadget I would buy if it came with an 8 hour battery life).

Play is IPv6 connected and I have v6 at home, in the datacentre and at work so I can quickly spin up daemons for testing without having to worry about forwarding ports, and it&rsquo;s all firewalled off to trusted locations.

From everywhere else, I can SSH tunnel my VNC session and reap most of the benefits, meaning I can work from basically any computer with a copy of VNC on it. A handy tips for OSX machines is that you can run

<div class="codehilite">
  <pre>open <span class="s1">'vnc://[2a01:348:2e0:dead::6]:5902/'</span>
</pre>
</div>

to bring up the built-in VNC client.

Outside of terminal work, having a separate Chromium install you can use from another machine is great when you don&rsquo;t trust the browser on the random machine you happen to be using, or when you want to see the view of a site from &ldquo;outside&rdquo; of your current network.

 [1]: https://insm.cf/=/d428c1c7.png
 [3]: http://www.pcmag.com/slideshow_viewer/0,3253,l=256274&a=256274&po=2,00.asp
 [4]: https://www.iweb-hosting.co.uk/
 [5]: https://smtpd.github.io/qpsmtpd/
 [6]: http://www.tightvnc.com/vncserver.1.php
 [7]: http://xwinman.org/mwm.php
 [8]: http://www.bittorrent.com/sync


