---
title: Tilde Beat Clock
date: 2015-12-09
layout: post
---

On [tilde.town][tt], we measure time in [Swatch Internet Time][sit], or Beats. [^1]


![Tilde Clock](https://farm1.staticflickr.com/637/23262927919_fcd233e3aa_b.jpg)

Projects look so pretty until the business of using wires to connect everything
up happens.

I've got a [real time clock][rtc] (which comes with 64k of EEPROM, bonus?) and
I'm planning on using an NXP 74HC595 shift register to sink current from the
common-anode 7-segment LED displays I'm using. Three pins on the ATmega328 will
source current for the displays. Only one display will be on at a time.

If it doesn't flicker too much, I'd like to just have one segment on at a time
- each "frame" we'll shift in a pattern that lights one segment, and then turn
on current to that display, then everything goes off again and the process
starts over.

[tt]: http://tilde.town/
[sit]: https://en.wikipedia.org/wiki/Swatch_Internet_Time
[rtc]: http://www.hobbyist.co.nz/?q=real_time_clock

[^1]: Yeah we don't *really* adhere to this, but *I* have my IRC client set to beats and various bots will tell you the time in beats, so I'm rolling with it.
