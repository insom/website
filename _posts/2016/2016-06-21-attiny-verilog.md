---
date: "2016-06-21T20:01:32Z"
title: "ATtiny, Verilog, Oscilloscopes"
type: "journal"
layout: post
---

One of the things I didn't cover in my last post was my problems flashing an
ATtiny461. It just wouldn't take, and even my spare wouldn't. It's probably me,
but as a friend was placing an order with a UK supplier, I thought I'd
piggyback on that and get an ATtiny85 - a more suitable chip [for what I had in
mind][m].

[m]: https://insom.github.io/project/atx/

It's a little unfortunate that I named the project attiny461-atx. Whoops! I've
created a [branch with the '85 compatible code on it][b]. Because this chip
really *is* tiny, it only has a PORTB. My previous code took some liberties by
using each of PORTA and PORTB for input and output respectively, and I've
tidied those up in my latest commits.

[b]: https://github.com/insom/attiny461-atx/tree/attiny85

![Chip with Programmer](https://c6.staticflickr.com/8/7069/27823752525_22c828c73b_b.jpg)

An IDC10 to breadboard adaptor has once again proven to be a great purchase. I
think I might pick up IDC to breadboard adaptors in a variety of pin counts,
even. This suits so well because the USBasp clone that I'm using defaults to a
10 pin layout.

PB4 is connected to an LED and PB3 to a switch with pull-ups enabled, and then
on to ground. PB4 will be brought high to simulate the PSU coming on, but in
the final circuit it's actually going to be pulling the pin down, as that's
what triggers an ATX PSU to power on.

I can't continue tonight as I sold my spare IEC leads at the weekend, but
hopefully I'll nail this at lunch tomorrow using Boo-the-Power-Supply.

<hr>

It's been a busy day, electronics-wise: Bas, Jon and I got some "Hello, World"
Verilog up and running on an [FPGA board I ordered][fpga] (harder than it sounds,
easier than I thought it would be), and I even had time to flash a newer
firmware onto my [DSO138 scope kit][dso].

[fpga]: http://www.aliexpress.com/item/xilinx-fpga-development-board-spartan6-xilinx-spartan-6-XC6SLX45-xilinx-board-xilinx-spartan-6/967529392.html
[dso]: http://www.jyetech.com/Products/LcdScope/e138.php

It turns out it runs the same CPU as the boards I've been running Forth on, so
the process of flashing it was pretty straightforward, though instead of two
jumpers you need to solder two sets of pads together, then remove the solder
blobs after programming. Perhaps a little less user friendly.

Now, it can auto-centre its trigger. Here's a shot of one of the output pins
from the 74HC374 on my Z80 - including the duty cycle and frequency counter
that I've only just discovered are included:

![11Hz](https://c1.staticflickr.com/8/7123/27211553264_3e9738212f_b.jpg)

In other words, it takes 45 milliseconds to get from [line 4 to line 15 of this program][l].

[l]: https://github.com/insom/LittleComputer/blob/master/ASM/Flasher/flasher.asm#L4:L15
