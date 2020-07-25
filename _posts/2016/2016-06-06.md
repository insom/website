+++
date = "2016-06-06T21:04:29Z"
title = "Forth: Nokia LCD (finale)"
type = "journal"
+++

I got my [Forth green square][fgs].

![Mecrisp Hello World](https://camo.githubusercontent.com/a2d558dab1f6c50a3efc09926f49a1988ebc1970/687474703a2f2f31376b2e756b2f732f63353031326663632e706e67)

Bas' and my LCD driver for the PCD8544 display is now in the upstream Embello
repository. The API it exports to the `graphics.fs` library is just three
words:

    : putpixel ( x y -- ) ;
    : clear ( -- ) ;
    : display ( -- ) ;

Of course, there's quite a bit under the hood. `putpixel` was challenging and
he fact that `dup dup` and `2dup` do very different things was time consuming
to find, but now it's done.

I love this environment and have given [AmForth][amf] a go on a spare Arduino
Uno. Using AmForth as a read-eval-print-loop allowed for interactively
exploring an STP16CL596 (16 bit shift register / current sink) hooked up to
a common anode LED matrix (5x7).

It's slow. *Way* slower than Mecrisp, but then the CPU is 8bit instead of
32bit and the clock is only 16MHz instead of 72Mhz, so that's to be expected
really. It's still as low level though, let's set PORTD pins 2 through 6 to
output, then turn on PD2

    $7C DDRD c!
    $4 PORTD c!

Okay, so this is just the same as

    DDRD = 0x7c;
    PORTD = 0x4;

in C, but the important part is there was no compilation step inbetween - just
poke bits of RAM and see what happens - if anything goes wrong, just hit reset
and try again.

Unfortunately the speed *is* an issue. Bas plans to drive the matrix display
with persistence of vision, and neither of us thinks we can optimise the Forth
enough to make that work at just 16Mhz.

Back to C, it is.

[fgs]: https://github.com/jeelabs/embello/pull/26
[amf]: http://amforth.sourceforge.net/
