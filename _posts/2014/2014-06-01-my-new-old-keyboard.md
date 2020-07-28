---
title: My New Old Keyboard
date: 2014-06-01
layout: post
---
Coming up on two years ago, [Nick][1] (our Managing Director at work) ordered this:

![New Apple Keyboard][2]

and got this:

![20 Year Old Apple Keyboard][3]

It&rsquo;s definitely one of the funniest cases of Amazon product substitution that I&rsquo;ve seen, and due to massive amount of badly-written robots crawling Amazon listings and fuzzily matching ASINs up to their own catalogues, it may not be unique.

No one wanted to deal with packaging up and raising customer service tickets with Amazon for the sake of a keyboard, so Nick ordered an official keyboard and let me keep the design classic<sup id="fnref-1"><a class="footnote-ref" href="#fn-1" rel="footnote">1</a></sup> that is my Apple Extended II keyboard.

I grabbed the [Apple IIgs hardware reference][4] from some web page somewhere, and digested the [Microchip ADB interfacing tech-note][5]. I found and pored over someone else&rsquo;s [ADB Arduino code][6], and I wrote quite a bit of timing specific Arduino code but never got very far. I managed to _send_ instructions over ADB &#8211; turning on and off the caps-lock light &#8211; but never once managed to read a keystroke.

I had followed [the `tmk_keyboard` discussion on GeekHack][7] and starred the [project on GitHub][8]. It relied on a [Teensy 2.0][9], which aren&rsquo;t available cheaply (or, at least, as cheaply as I would like) in the UK. Early versions needed the Teensy because they used the PJRC USB stack, which I believe is only (legally) available on a Teensy board.

Lots of time has passed, and I checked back in on GitHub to see that an alternative USB stack is now supported: [LUFA][10]. This means that you can run `tmk_keyboard` on any compatible ATMega device. Looking at the available clones I picked out a [not-quite-Arduino Pro Micro][11] and waited patiently for it to arrive.

It arrived.

Sadly, in the mean time I had started _another_ electronics project at work, and have left the only other Arduino I have there, along with my [Bus Pirate][12]. I had planned on using either the [ArduinoISP][13] sketch or the Bus Pirate to program the firmware straight over the top of whatever is included on the Pro Micro out of the box, but wasn&rsquo;t about to make the trip to work to do it.

I also wasn&rsquo;t really keen on waiting either.

The Pro Micro ships with a bootloader that appears as a AVR109 compatible programmer. This might be a one-time shot I had at this, but I was happy to take that chance as I could always unbrick the device when I got my hands on a proper programmer.

Building the firmware, I should point out, was really simple. I got the cross [development tools][14] that the [README][15] recommended, commented out some features from the `Makefile` that I felt I didn&rsquo;t want to spend any RAM on, and I ran `make`. It spat out a .hex file ready to write.

I got the command line ready in my terminal

<div class="codehilite">
  <pre><span class="n">sudo</span> <span class="n">avrdude</span> <span class="o">-</span><span class="n">P</span> <span class="o">/</span><span class="n">dev</span><span class="o">/</span><span class="n">tty</span><span class="p">.</span><span class="n">usbmodem</span><span class="o">*</span> <span class="o">-</span><span class="n">p</span> <span class="n">atmega32u4</span> <span class="o">-</span><span class="n">cavr109</span> \
    <span class="o">-</span><span class="n">v</span> <span class="o">-</span><span class="n">v</span> <span class="o">-</span><span class="n">v</span> <span class="o">-</span><span class="n">e</span> <span class="o">-</span><span class="n">U</span> <span class="n">flash</span><span class="o">:</span><span class="n">w</span><span class="o">:</span><span class="n">adb_usb_lufa</span><span class="p">.</span><span class="n">hex</span>
</pre>
</div>

and brought `RST` down to ground twice. This last step is covered in the unbricking guide for this Arduino, but I had to do it in order for `avrdude` to even see the device.

Unplugging the cable and plugging it into my Linux box heeded this fist-pump success moment:

<div class="codehilite">
  <pre><span class="p">[</span> <span class="mf">9088.741998</span><span class="p">]</span> <span class="n">hid</span><span class="o">-</span><span class="n">generic</span> <span class="mo">0003</span><span class="o">:</span><span class="n">FEED</span><span class="o">:</span><span class="mi"></span><span class="n">ADB</span><span class="mf">.0005</span><span class="o">:</span> <span class="n">input</span><span class="p">,</span><span class="n">hidraw0</span><span class="o">:</span> <span class="n">USB</span> <span class="n">HID</span> <span class="n">v1</span><span class="mf">.11</span> <span class="n">Keyboard</span> <span class="p">[</span><span class="n">t</span><span class="p">.</span><span class="n">m</span><span class="p">.</span><span class="n">k</span><span class="p">.</span> <span class="n">ADB</span> <span class="n">keyboard</span> <span class="n">converter</span><span class="p">]</span> <span class="n">on</span> <span class="n">usb</span><span class="o">-</span><span class="mo">0000</span><span class="o">:</span><span class="mo">00</span><span class="o">:</span><span class="mi">1</span><span class="n">d</span><span class="mf">.1</span><span class="o">-</span><span class="mi">1</span><span class="o">/</span><span class="n">input0</span>
</pre>
</div>

The board was alive; I hadn&rsquo;t bricked it and it came up with the right USB identifiers! I then proceeded to have some pain with pull-up resistors (I didn&rsquo;t have the right ones to hand, I made do, they were wrong) and had to make some use of the [`hid_listen`][16] command to get debugging output from the board.

[ Also, isn&rsquo;t it cool that you can basically get a _console_ from your keyboard firmware? Powerful devices are so cheap. ]

I wrote out the standard, correct test:

<div class="codehilite">
  <pre><span class="n">The</span> <span class="n">quic</span> <span class="n">brown</span> <span class="n">fox</span> <span class="n">jumps</span> <span class="n">over</span> <span class="n">the</span> <span class="n">lazy</span> <span class="n">dog</span><span class="p">.</span>
</pre>
</div>

Hm.

So, it looks like at some point in the last 20 years, someone has damaged the `k` key. This keyboard is really serviceable, so I was able to undo _one_ screw and two clips and have the thing flipped over, solder side up.

![Picture of PCB][17]

Checking the points for the `k` with my meter shows it was never registering a click. I desoldered it following a [guide to repair ALPS white switches][18] &#8211; but it was too damaged. I&rsquo;ve swapped it with `F15`, leaving me with a temporary unsightly gap.

I now have a fully functioning twenty year old _loud_ mechanical keyboard. All that remains is to make a decent case for the adaptor.

### Misc Gallery Shots {#misc-gallery-shots}

Current Status:

![Current Status][19]

Patching into an RC car&rsquo;s resistors<sup id="fnref-2"><a class="footnote-ref" href="#fn-2" rel="footnote">2</a></sup>:

![OMG OH NOES][20]

<div class="footnote">
  <hr />

  <ol>
    <li id="fn-1">
      I got free tickets to the Design Museum in London last year, and they literally had one of these keyboard on display, next to the also iconic but <em>much</em> less pleasant to use ADB mouse.&nbsp;<a class="footnote-backref" href="#fnref-1" rev="footnote" title="Jump back to footnote 1 in the text">&#8617;</a>
    </li>
    <li id="fn-2">
      Yes, really. My desperation at not being able to find a 1K resistor for a 5V pull-up lead to me patching into the resistors soldered on to other items. Not proud. Well. A little proud.&nbsp;<a class="footnote-backref" href="#fnref-2" rev="footnote" title="Jump back to footnote 2 in the text">&#8617;</a>
    </li>
  </ol>
</div>

 [1]: https://twitter.com/nickpinson
 [2]: https://insm.cf/=/apple-bt.jpeg
 [3]: https://insm.cf/=/apple-extended-keyboard-ii.jpeg
 [4]: https://archive.org/details/Apple_IIgs_Hardware_Reference
 [5]: http://www.microchip.com/stellent/idcplg?IdcService=SS_GET_PAGE&nodeId=1824&appnote=en011062
 [6]: https://gitorious.org/arduino-adb
 [7]: http://geekhack.org/index.php?topic=14290
 [8]: https://github.com/tmk/tmk_keyboard/
 [9]: https://www.pjrc.com/teensy/
 [10]: http://www.fourwalledcubicle.com/LUFA.php
 [11]: https://www.sparkfun.com/products/12640
 [12]: http://dangerousprototypes.com/docs/Bus_Pirate
 [13]: http://arduino.cc/en/Tutorial/ArduinoISP
 [14]: http://www.obdev.at/products/crosspack/index.html
 [15]: https://github.com/tmk/tmk_keyboard/blob/master/doc/build.md
 [16]: http://www.pjrc.com/teensy/hid_listen.html
 [17]: https://insm.cf/=/c7c82c85.png
 [18]: https://68kmla.org/forums/index.php?/topic/13901-how-to-repair-an-alps-keyswitch-in-15-steps/
 [19]: https://insm.cf/=/6fa571b8.png
 [20]: https://insm.cf/=/5ad0f9f1.png


