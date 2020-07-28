---
title: 'LindyPi Build- Software'
date: 2013-06-10
layout: post
---
Following on from the fairly [straightforward build process][1] of building my new Raspberry Pi server, I thought I&rsquo;d document the software stack too.

My [previous, Intel, server][2] had several LXC containers dedicated to different tasks. I sometimes give access to my home server to other people, and I run some pieces of software which have conflicting or many dependencies and my obsessive tendency makes we want to keep them apart.

Examples include an X desktop environment, and anything of significant size written in Ruby or Python, which tends to sprout `-dev` dependencies so they can be built by `gem` or `pip`. `virtualenv` and `rbenv` don&rsquo;t help you manage these external dependencies. Most people might consider a whole separate Debian install overkill, if you do, too, then this page is probably not for you.

Given that I only had 512Mb of RAM to play with on the Pi, and not the 2Gb I had on the Intel machine, I didn&rsquo;t want to add the overhead of libvirt and its associated daemons. I also didn&rsquo;t want to run through the whole init process when all I really want is a couple of specific daemons and a separate network environment. Finally, I&rsquo;m not bothered about limiting memory usage, and the memory cgroup driver has enough overhead to be disabled by default in Debian. I&rsquo;ve not done any benchmarks, but I think the little ARMv6 in the Pi needs all the help it can get.

At $WORK we&rsquo;re using the libvirt LXC stack rather than the Debian/Ubuntu LXC package, because we had existing libvirt experience from KVM. Sadly, getting libvirt LXC working the way that we wanted required a fair bit of reading the source code. Luckily, that started to open my eyes to how easy this LXC stuff really was. I hacked the bare minimum together one evening:

<blockquote class="twitter-tweet">
  <p>
    <a href="https://t.co/eFWQRP3uGT" title="https://gist.github.com/insom/5528775">gist.github.com/insom/5528775</a> Getting some C on so I can bring up little LXC containers without libvirt or the Debian LXC package.
  </p>

  <p>
    &mdash; Aaron Brady (@insom) <a href="https://twitter.com/insom/status/331536971954524160">May 6, 2013</a>
  </p>
</blockquote>



Just enough to get a separate process namespace going. A few night&rsquo;s later I had [a container with networking and a getty][3] and I was closer to done than I thought at the time. I&rsquo;d started to go down the rabbit-hole of `getty` and terminal control and `select`, when really all I wanted was a machine that was network accessible enough to run SSH.

I needed to do a bit more work around filesystem isolation, after you calling `pivot_root` you still need to unmount all of the old filesystems, in reverse-length-order. That is; the deepest mounts before the shallow ones. I straight-up lifted some code from libvirt to do this, which is why [my whole programme][4] is now LGPL licensed and blessed with an IBM/RedHat/LGPL copyright statement which almost doubles its length.

The full [C source is available here][4].

The two main parts of interest operate in two different threads, one of which is in the &ldquo;real world&rdquo; of the bare OS, and one of which is executing within an LXC context.

<div class="codehilite">
  <pre><span class="n">snprintf</span><span class="p">(</span><span class="n">buf</span><span class="p">,</span> <span class="n">BUFSIZ</span><span class="p">,</span> <span class="s">"ip link add name %s type veth peer name slave"</span><span class="p">,</span> <span class="n">v</span><span class="p">[</span><span class="mi">1</span><span class="p">]);</span>
<span class="n">system</span><span class="p">(</span><span class="n">buf</span><span class="p">);</span>
<span class="n">snprintf</span><span class="p">(</span><span class="n">buf</span><span class="p">,</span> <span class="n">BUFSIZ</span><span class="p">,</span> <span class="s">"ip link set dev %s up"</span><span class="p">,</span> <span class="n">v</span><span class="p">[</span><span class="mi">1</span><span class="p">]);</span>
<span class="n">system</span><span class="p">(</span><span class="n">buf</span><span class="p">);</span>
<span class="n">snprintf</span><span class="p">(</span><span class="n">buf</span><span class="p">,</span> <span class="n">BUFSIZ</span><span class="p">,</span> <span class="s">"brctl addif br1 %s"</span><span class="p">,</span> <span class="n">v</span><span class="p">[</span><span class="mi">1</span><span class="p">]);</span>
<span class="n">system</span><span class="p">(</span><span class="n">buf</span><span class="p">);</span>
<span class="n">sleep</span><span class="p">(</span><span class="mi">5</span><span class="p">);</span> <span class="c1">// Give the bridge a chance to spin up</span>
<span class="n">pid</span> <span class="o">=</span> <span class="n">clone</span><span class="p">(</span><span class="n">child</span><span class="p">,</span> <span class="n">stacktop</span><span class="p">,</span> <span class="n">cflags</span><span class="p">,</span> <span class="n">pointer</span><span class="p">);</span>
<span class="n">snprintf</span><span class="p">(</span><span class="n">buf</span><span class="p">,</span> <span class="n">BUFSIZ</span><span class="p">,</span> <span class="s">"ip link set slave netns %d"</span><span class="p">,</span> <span class="n">pid</span><span class="p">);</span>
<span class="n">system</span><span class="p">(</span><span class="n">buf</span><span class="p">);</span>
</pre>
</div>

Briefly, on the outside, I create a `veth` pair, two virtual Ethernet devices linked by an imaginary piece of string. One is called after the container&rsquo;s name, the other is always called &ldquo;slave&rdquo;. Then I set it &ldquo;up&rdquo;, and add it to a bridge (hardcoded to suit my needs). Despite disabling spanning-tree protocol, I still had better results sleeping for a few seconds here, and then I call `clone` with the magic LXC flags and get a new thread in a new namespace. Finally, I move the &ldquo;slave&rdquo; NIC into a different networking namespace, from the outside, and exit.

<div class="codehilite">
  <pre><span class="n">snprintf</span><span class="p">(</span><span class="n">buf</span><span class="p">,</span> <span class="n">BUFSIZ</span><span class="p">,</span> <span class="s">"/lxc/%s/.old"</span><span class="p">,</span> <span class="n">n</span><span class="p">);</span>
<span class="n">mkdir</span><span class="p">(</span><span class="n">buf</span><span class="p">,</span> <span class="mo">0700</span><span class="p">);</span>
<span class="n">snprintf</span><span class="p">(</span><span class="n">buf2</span><span class="p">,</span> <span class="n">BUFSIZ</span><span class="p">,</span> <span class="s">"/lxc/%s"</span><span class="p">,</span> <span class="n">n</span><span class="p">);</span>
<span class="n">pivot_root</span><span class="p">(</span><span class="n">buf2</span><span class="p">,</span> <span class="n">buf</span><span class="p">);</span>
<span class="n">chdir</span><span class="p">(</span><span class="s">"/"</span><span class="p">);</span>
<span class="n">mount</span><span class="p">(</span><span class="s">"/proc"</span><span class="p">,</span> <span class="s">"/proc"</span><span class="p">,</span> <span class="s">"proc"</span><span class="p">,</span> <span class="mi"></span><span class="p">,</span> <span class="nb">NULL</span><span class="p">);</span>
<span class="n">close</span><span class="p">(</span><span class="mi">2</span><span class="p">);</span>
<span class="n">close</span><span class="p">(</span><span class="mi">1</span><span class="p">);</span>
<span class="n">close</span><span class="p">(</span><span class="mi"></span><span class="p">);</span>
<span class="n">unmount_old</span><span class="p">();</span>
<span class="n">mount</span><span class="p">(</span><span class="s">"devpts"</span><span class="p">,</span> <span class="s">"/dev/pts"</span><span class="p">,</span> <span class="s">"devpts"</span><span class="p">,</span> <span class="mi"></span><span class="p">,</span> <span class="s">"newinstance,ptmxmode=0666,mode=0620,gid=5"</span><span class="p">);</span>
<span class="n">execl</span><span class="p">(</span><span class="s">"/sbin/init"</span><span class="p">,</span> <span class="s">"/sbin/init"</span><span class="p">,</span> <span class="p">(</span><span class="kt">char</span> <span class="o">*</span><span class="p">)</span><span class="nb">NULL</span><span class="p">);</span>
<span class="n">perror</span><span class="p">(</span><span class="nb">NULL</span><span class="p">);</span>
<span class="k">return</span> <span class="mi"></span><span class="p">;</span>
</pre>
</div>

In the container, I create somewhere to move the existing root to, within the new root, which I&rsquo;ve hardcoded as &ldquo;/lxc/$containername&rdquo;. Once we&rsquo;ve pivoted, we change page to &ldquo;/&rdquo; because our current working directory is undefined, mount `/proc` because various things expect it, close our file descriptors (which may relate to a terminal on the outside, which would be bad), create a new `devpts` filesystem instance and finally, execute init, letting it take over our process. We never actually hit the `perror` or `return` unless the `execl` call fails.

**Addendum**: I forgot to mention, you&rsquo;ll need to add some missing functionality into the Raspbian kernel, primarily `veth` device support. I followed [these steps from Yohei Kuga][5], though I think CONFIG_VETH was all I actually had to change.

<div class="codehilite">
  <pre><span class="gd">--- .config.old 2013-05-18 11:20:10.000000000 +0000</span>
<span class="gi">+++ .config 2013-05-18 15:11:11.000000000 +0000</span>
<span class="gu">@@ -1211,7 +1211,7 @@</span>
 # CONFIG_NETPOLL_TRAP is not set
 CONFIG_NET_POLL_CONTROLLER=y
 CONFIG_TUN=m
<span class="gd">-# CONFIG_VETH is not set</span>
<span class="gi">+CONFIG_VETH=m</span>

 #
 # CAIF transport drivers
</pre>
</div>

_Pro tip_: Do not do your git checkout of the very large Linux kernel tree on the Pi; if at all possible, check it out on a more powerful machine and then rsync the files across. That said, if you do it from a Mac OS X install which has a case insensitive filesystem, you&rsquo;ll probably need to `git reset --hard` to fix the mangled filenames, which will take a surprisingly long time.

Also: budget about a day for the kernel compile.

Now we need somewhere to pivot _to_. I use a [USB connected HDD with LVM][1], so I create new filesystem, mount it where I want it, and put an empty Debian on there:

<div class="codehilite">
  <pre>lvcreate -L 10G -n one WDG
mkfs.ext4 /dev/WDG/one
mkdir -p /lxc/one
mount /dev/WDG/one /lxc/one
debootstrap wheezy /lxc/one --include<span class="o">=</span>ssh
</pre>
</div>

[Time passes.][6]

Now you&rsquo;ll need to do some initial configuration:

<div class="codehilite">
  <pre><span class="nb">echo </span>one &gt; /lxc/one/etc/hostname
cat &gt; /lxc/one/etc/hosts <span class="s">&lt;&lt;EOF</span>
<span class="s">127.0.0.1 localhost localhost.localdomain</span>
<span class="s">127.0.1.1 one one.insom.me.uk</span>
<span class="s">EOF</span>
cat &gt; /lxc/one/etc/inittab <span class="s">&lt;&lt;EOF</span>
<span class="s">rc::bootwait:/etc/rc</span>
<span class="s">id:2:initdefault:</span>
<span class="s">ssh:2:respawn:/usr/sbin/sshd -D</span>
<span class="s">EOF</span>
cat &gt; /lxc/one/etc/rc <span class="s">&lt;&lt;EOF</span>
<span class="s">#!/bin/sh</span>
<span class="s">/bin/hostname one</span>
<span class="s">/sbin/ip link set dev lo up</span>
<span class="s">/sbin/ip link set dev slave up</span>
<span class="s">/sbin/ip addr add 192.168.1.3/24 dev slave</span>
<span class="s">/sbin/ip route add default via 192.168.1.1</span>
<span class="s">/sbin/ip -6 addr add 2a01:348:2e0:cfff::3/64 dev slave</span>
<span class="s">/sbin/ip -6 route add default via 2a01:348:2e0:cfff::1</span>
<span class="s">EOF</span>
chmod a+x /lxc/one/etc/rc
</pre>
</div>

That&rsquo;ll set up a basic network configuration and SSH on boot. You won&rsquo;t be able to login as root because it doesn&rsquo;t have a password, so lets set one, by running `passwd` in the new filesystem:

<div class="codehilite">
  <pre>chroot /lxc/one passwd root
</pre>
</div>

If you followed the above, you should even be able to run your new container. Compile the [C attached to the main gist][4] and run it as root with &ldquo;one&rdquo; as its first parameter, and enjoy the fruits of your effort:

<div class="codehilite">
  <pre><span class="c"># ./lxc-run one</span>
<span class="c"># ps axwf</span>
...
15645 ?        Ss     0:00 init <span class="o">[</span>2<span class="o">]</span>
15660 ?        Ss     0:00  <span class="se">\_</span> /usr/sbin/sshd -D
...
<span class="c"># ssh root@192.168.1.3</span>
Warning: Permanently added <span class="s1">'192.168.1.3'</span> <span class="o">(</span>ECDSA<span class="o">)</span> to the list of known hosts.
root@192.168.1.3<span class="err">'</span>s password:
Linux pi 3.6.11+ <span class="c">#2 PREEMPT Mon May 20 14:05:58 UTC 2013 armv6l</span>

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms <span class="k">for </span>each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
root@one:~# ps axwf
  PID TTY      STAT   TIME COMMAND
    1 ?        Ss     0:00 init <span class="o">[</span>2<span class="o">]</span>
   12 ?        Ss     0:00 /usr/sbin/sshd -D
   13 ?        Ss     0:00  <span class="se">\_</span> sshd: root@pts/2
   14 pts/2    Ss     0:00      <span class="se">\_</span> -bash
   20 pts/2    R+     0:00          <span class="se">\_</span> ps axwf
</pre>
</div>

(We&rsquo;ve upped the pid count a bit because we executed all of those commands in `/etc/rc`, remember? That&rsquo;s why `sshd` isn&rsquo;t pid #2).

 [1]: /post/lindy-pi-1/hardware
 [2]: https://www.flickr.com/photos/insomnike/8928905212/
 [3]: https://gist.github.com/insom/5551176
 [4]: https://gist.github.com/insom/5749718
 [5]: https://plus.google.com/113091037050058478853/posts/8tYdBrbxu8i
 [6]: http://steel.lcc.gatech.edu/~marleigh/zork/transcript.html


