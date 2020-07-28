---
title: Retrochallenge 2014 Winter Warm-up
date: 2014-01-05
layout: post
---
After a [PINE-related conversation][1] with [Twylo][2], I&rsquo;ve made a [late entry to Retrochallenge&rsquo;s 2014 Winter Warmup][3]:

>   * setting up a dumb terminal (I&rsquo;m planning on using a Raspberry Pi booting straight into a single-user-mode Minicom session, which would make a cheap PockeTerm alternative.) and use only an 80&times;25 text session for interacting with:
>   * an emulated &rsquo;96-era Unix. Possibly Redhat 3.0.3 under i386. I also used Solaris and Ultrix on SparcStation and DECstations around this time (this was practically retrocomputing when I was doing it the first time!) &ndash; maybe getting one or other of these working under QEMU leading to:
>   * using a PPP session from the emulated Unix as my main way of interacting with the social world: updating my blog, reading my email (delivered in batch via UUCP or POP3), Twitter (anachromism), IRC.
>
> In summary: a terminal-only interface to an old Unix using serial as its only access to the outside world.

I&rsquo;m happy to report some success on the first point: I have a Raspberry Pi booting straight into a fullscreen 80x25ish<sup id="fnref-1"><a class="footnote-ref" href="#fn-1" rel="footnote">1</a></sup> Minicom session, over an actual serial port. It&rsquo;s as close to a [PockeTerm][4] as I could make: low resolution, over actual RS232, and not running a full Unix environment in the background (if you could run `ps`, process #1 would be minicom).

Ideally, I would like to have avoided using a USB serial adaptor: the Pi has a UART on board running at 3.3v, and this can be converted to a proper serial port via a MAX232 IC ([here&rsquo;s a guide][5]). Unfortunately that would mean buying new parts, which would delay me starting (and it&rsquo;s January and I&rsquo;m moving home, and the budget for retrocomputing supplies is approximately &pound;0).

Here&rsquo;s a guide to turn this:

![RaspberryPi Bits][6]

into this:

![RaspberryPi Terminal][7]

(Ultimately to connect to this):

![N270 Board][8]

Start with [a Raspbian Wheezy image][9], boot to a console and then:

<div class="codehilite">
  <pre><span class="c"># install minicom</span>
sudo apt-get install minicom
<span class="c"># pick a more suitable font</span>
sudo dpkg-reconfigure console-setup
</pre>
</div>

I picked VGA 16&#215;32 &#8211; on a 1280&#215;1024 screen that gives me 80&#215;32 characters.

We&rsquo;re going to create a replacement for `/sbin/init`, but that means we&rsquo;ll need to do all of our own set up and also that we won&rsquo;t go through the normal system initialisation, including: mounting the filesystem read-write, setting the fonts, loading kernel modules and having `devfs` available.

I&rsquo;m using a [Prolific 2303 USB serial adaptor][10], so I need to load the `pl2302` driver, create the `/dev/ttyUSB0`-equivalent device, too. Because `/dev` is a different filesystem, let&rsquo;s just be lazy and put it in `/`.

The device numbers are `188` and ``, so before rebooting:

<div class="codehilite">
  <pre>sudo mknod /USB c 188 0
sudo vi /init
</pre>
</div>

You might also want to set the defaults for Minicom, as root, while you can still write to the disk. Change your device (under A) to `/USB`, set your baud and flow control to match what you&rsquo;re connecting to (I&rsquo;m going with 9600 here, and I only have a 3-wire serial lead, so I&rsquo;m using software flow control, too). &ldquo;Save setup as dfl&rdquo; to save &hellip; as &hellip; the &hellip; default.

<div class="codehilite">
  <pre>sudo minicom -s
</pre>
</div>

Then we&rsquo;ll create our new init, as `/init`:

<div class="codehilite">
  <pre><span class="c">#!/bin/sh</span>
/sbin/modprobe pl2303
/bin/setupcon
<span class="nb">exec</span> /usr/bin/minicom -s -c on
</pre>
</div>

(Make sure to make it executable)

<div class="codehilite">
  <pre>sudo chmod 755 /init
</pre>
</div>

Then change the init in `/boot/cmdline.txt` &#8211; add `init=/init` to the end of whatever is currently in there and reboot!

If the stars align and you have the configuration I do, you will have a terminal the boots up in about 3 seconds.

If you exit Minicom, the kernel will panic- but that&rsquo;s okay: you can just power it off when you&rsquo;re done. The disk is never mounted read-write, so you&rsquo;re not going to need to worry about wearing out your SD card, either.

<div class="footnote">
  <hr />

  <ol>
    <li id="fn-1">
      The font I was able to use gives me 80&#215;32, but it looks suitably retro compared to the sharp high-resolution displays we&rsquo;re spoiled with nowadays.&nbsp;<a class="footnote-backref" href="#fnref-1" rev="footnote" title="Jump back to footnote 1 in the text">&#8617;</a>
    </li>
  </ol>
</div>

 [1]: https://twitter.com/insom/status/419258875758788608
 [2]: https://twitter.com/Twylo
 [3]: http://www.wickensonline.co.uk/retrochallenge-2012sc/2014-winter-warmup-entrants-list/
 [4]: http://www.brielcomputers.com/wordpress/?cat=25
 [5]: http://www.davidhunt.ie/?p=3091
 [6]: https://insm.cf/=/f164d156.png
 [7]: https://insm.cf/=/6e19782b.png
 [8]: https://insm.cf/=/b7746bbe.png
 [9]: http://www.raspberrypi.org/downloads
 [10]: http://www.amazon.co.uk/gp/product/B00425S1H8


