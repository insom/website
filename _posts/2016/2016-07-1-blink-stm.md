---
date: "2016-07-01T12:00:00Z"
title: "Program 'Hello World' to an STM32F103C8, without an ST-Link"
type: "journal"
layout: post
---

In May, Kevin Cuzner [posted instructions on bootstrapping a Cortex M3
microcontroller without a dev board][db]. It hit Hackaday and grabbed my
attention because I happened to have a couple of those chips on boards I'd been
using to play with Forth.

[db]: http://kevincuzner.com/2016/05/22/dev-boards-where-were-going-we-wont-need-dev-boards/

He's done the hard work of carving the neccessary include files out of ST's
SDK, and wraps the whole thing up in an easy to use `Makefile`. Great!
I made one little tweak (for [Ubuntu Xenial support][xen]), and it all builds
smoothly.

[xen]: https://github.com/kcuzner/stm32f103c8-blink/pull/1

He's included an `openocd.cfg` config file, but I don't have an ST-Link device
to load the output with. Luckily, you can kind of smush the instructions
[Jean-Claude Wippler put together][jcw] to upload your program.

[jcw]: http://jeelabs.org/book/1546c/

Grab `stm32loader` from
[GitHub](https://raw.githubusercontent.com/jsnyder/stm32loader/master/stm32loader.py).
Put `BOOT0` in the 1 position, and `BOOT1` in the 0 position. Reset your board
and run the following to upload the .bin that `make` generated to 0x80000000.

    lappy:~/Repo/stm32f103c8-blink aaron$ python stm32loader.py -a 0x08000000 \
        -g 0x08000000 -p /dev/ttyUSB0 -e -w bin/blink.bin
    Bootloader version 22
    Chip id: 0x410 (STM32 Medium-density)
    Write 256 bytes at 0x8000000
    Write 256 bytes at 0x8000100
    Write 256 bytes at 0x8000200
    Write 256 bytes at 0x8000300
    Write 256 bytes at 0x8000400
    Write 256 bytes at 0x8000500
    Write 256 bytes at 0x8000600
    Write 256 bytes at 0x8000700
    Write 256 bytes at 0x8000800
    Write 256 bytes at 0x8000900
    Write 256 bytes at 0x8000A00
    Write 256 bytes at 0x8000B00

And you're done! I can confirm that I have a blinking LED on port PB0.
