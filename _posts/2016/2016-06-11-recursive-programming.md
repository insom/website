---
date: "2016-06-11T19:06:29Z"
title: "Recursive ATmega programmer programming"
type: "journal"
layout: post
---

I am become yak, destroyer of progress.

I was playing with one of my left-over populated [Radio 1][r1] boards. I've
recently gotten a USBasp (knock-off) from eBay and back when I was designing
the board I actually thought ahead. I put a standard 6-pin programming header
on the board, even though I was just using a Bus Pirate to flash them.

I wasn't sure what state the fuses and firmware were in, so I read them with
`avrdude` and plugged them into an online fuse calculator. That's when I saw
you can actually clock these down to 128KHz on the internal RC oscillator.
Interesting! The board was running a version of the Arduino `blink` sketch
anyway - how slow is 128KHz? So, I set the fuses to find out:

	% avrdude -c usbasp-clone -p m328p -U lfuse:w:0xe3:m
	avrdude: warning: cannot set sck period. please check for usbasp firmware update.
	avrdude: AVR device initialized and ready to accept instructions
	avrdude: writing lfuse (1 bytes)

(Check out that warning: it's going to be relevant in a minute).

![Flashing the Radio 1 board](https://c4.staticflickr.com/8/7129/27530528571_e90123f9cc_b.jpg)

Cool, so at this rate it takes an *age* to flash the LED. I'm not sure what I
was expecting. I'll just put it back how it was:

	% avrdude -c usbasp-clone -p m328p -U lfuse:w:0xe2:m
	avrdude: warning: cannot set sck period. please check for usbasp firmware update.
	avrdude: error: program enable: target doesn't answer. 1
	avrdude: initialization failed, rc=-1
			 Double check connections and try again, or use -F to override
			 this check.

Ruh-roh.

The 328 is now clocked too slow to speak SPI at the default rate, so I can't
flash it back. The USBasp is running too old a firmware to slow down its clock.
Now to begin "a game of programmers".

I need to use the USBasp to program a Boarduino with the Arduino firmware (it
previously had its Arduino bootloader wiped):

![ASP on Boarduino Action](https://c3.staticflickr.com/8/7262/27504075442_4f2cd13576_b.jpg)

Then I use the FTDI to put the ArduinoISP sketch on the Boarduino, and upload
[new firmware onto the USBasp][newf]:

![Revenge of the Boarduino!](https://c5.staticflickr.com/8/7193/27326404420_3c4f3662d9_b.jpg)

	% avrdude -c avrisp -p m8 -P /dev/ttyUSB0 -b 19200
	avrdude: AVR device initialized and ready to accept instructions
	Reading | ################################################## | 100% 0.02s
	avrdude: Device signature = 0x1e9307 (probably m8)

Now I can use the USBasp to fix the Radio 1 board:

	% avrdude -c usbasp -p m328p -U lfuse:w:0xe2:m -B 1000
	avrdude: set SCK frequency to 1000 Hz
	avrdude: AVR device initialized and ready to accept instructions
	avrdude: writing lfuse (1 bytes):

Success! Now I'm back at the beginning!

Well, while I've got all this kata in my head, I might as well put the Arduino
bootloader back on some other knock-offs:

![Deek Robot Arduino Mini](https://c5.staticflickr.com/8/7275/27504080972_6c065fb702_b.jpg)

Right, now I can get some work done. Oh. It's dark out. Maybe tomorrow.

[r1]: https://www.insom.me.uk/2014/09/radio/
[newf]: http://www.rogerclark.net/updating-firmware-on-usbasp-bought-from-ebay/
