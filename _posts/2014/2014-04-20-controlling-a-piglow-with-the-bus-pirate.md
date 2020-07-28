---
title: Controlling a PiGlow with the Bus Pirate
date: 2014-04-20
layout: post
---
<blockquote class="twitter-tweet" lang="en">
  <p>
    Also: for Pi day I got a PiBow, PiGlow and PiBrella!
  </p>

  <p>
    &mdash; Aaron Brady (@insom) <a
href="https://twitter.com/insom/statuses/444590498511347712">March 14, 2014</a>
  </p>
</blockquote>



(If it wasn&rsquo;t apparent: my birthday is on 14th March, the same day as [Pi Day][1] and [other celebrations][2])

Missed off of that list of presents: this year I got a [Bus **Pi**rate][3] from Dangerous Prototypes.

![The Bus Pirate][4]

The Bus Pirate is a single PCB diagnostic and development tool that speaks several serial protocols: SPI, I2C, 1-Wire, low-voltage RS232 and it can also perform some non-serial tasks, like reading an ADC or generating PWM signals.

Like many useful tools, it has a bit of a learning curve. There&rsquo;s [wiki pages with lots of information][5] but they are no substitute for just getting your hands dirty and using the thing. In fact, there&rsquo;s a [3EEPROM Explorer Board][6] for this very reason- it gives someone taking their Bus Pirate out of the box something to poke while they learn the ropes.

I didn&rsquo;t have one of these, but it turns out that doesn&rsquo;t matter: enter the [PiGlow][7].

![The PiGlow][8]

PiGlow provides 18 dimmable LEDs and is designed to be used with a Raspberry Pi. It sits right on the GPIO header of the Pi. It doesn&rsquo;t use actual GPIO pins though, because the PiGlow is actually based on the [SN3218 I2C PWM LED driver][9].

If you&rsquo;re following along, you&rsquo;ll need a few more bits to get up and running. I already had a breadboard-compatible breakout for the Raspberry Pi GPIO header (not exactly a [Cobbler][10], but similar), I needed [an IDC10 ribbon][11] and an [IDC10 breadboard breakout][12]. If you had a [Bus Pirate Cable][13] or even just female-to-male jumper wires, you could probably do without those two.

For the remaining hardware part, it&rsquo;s just a case of connecting everything up. I moved slowly here: because I&rsquo;d added in adaptors and ribbons cables (not all of which were keyed to avoid flipping them around) I had to check that the numbering of pins didn&rsquo;t get messed up from what I expected.

![Bus Pirate Pin Out][14]

(This pin out diagram from [Crockett Engineering][15] was extremely useful for this step)

For example, the first thing I did was put an LED across where I expected the `3.3V` and `GND` to be on my IDC10 breakout. Once you select a mode on the Bus Pirate, using the `V` command turns on the power supply and will light up the LED. This step-by-step testing paid off: _the LED did not light_, I had the pins all backwards. For _my_ set up, 9 was `3.3V` and 10 was `GND`.

Once that was established, I checked the image on the Dangerous Prototypes site for the `SDL` and `SDA` connections (3 and 4, respectively) and I also ran the `5V` (pin 8) over to pin 2 on the GPIO breakout.

I2C requires pull up resistors. As the Bus Pirate runs at both `3.3V` and `5V`, you will need to provide an input to `Vpu` on the board. I connected pin 6 on my breakout (`Vpu`) to pin 9 (`3.3V`).

![My Wiring][16]

(You can see my version of the wiring above: I have a lot more wires plugged in. I hooked up all of the `GND` and `3.3V` inputs before I realised which ones were needed and which weren&rsquo;t. You don&rsquo;t need to.)

<table border="1" cellpadding="5">
  <tr>
    <th colspan="2">
      Raspberry Pi Pins
    </th>
  </tr>

  <tr>
    <td>
      GND
    </td>

    <td>
      14
    </td>
  </tr>

  <tr>
    <td>
      5v
    </td>

    <td>
      2
    </td>
  </tr>

  <tr>
    <td>
      3.3v
    </td>

    <td>
      1, 17
    </td>
  </tr>

  <tr>
    <td>
      SDA
    </td>

    <td>
      3
    </td>
  </tr>

  <tr>
    <td>
      SCL
    </td>

    <td>
      5
    </td>
  </tr>
</table>

(Where 1 is the bottom left pin pictured above, 2 is the top left etc.)

Now, for software. I&rsquo;m driving this from a Debian Jessie laptop, but as long as you have USB serial port drivers, you could be driving it from anything.

Load `picocom`

<pre>sudo picocom --b 115200 /dev/ttyUSB0
picocom v1.7

port is        : /dev/ttyUSB0
flowcontrol    : none
baudrate is    : 115200
parity is      : none
databits are   : 8
escape is      : C-a
local echo is  : no
noinit is      : no
noreset is     : no
nolock is      : no
send_cmd is    : sz -vv
receive_cmd is : rz -vv
imap is        :
omap is        :
emap is        : crcrlf,delbs,

Terminal ready
</pre>

The Bus Pirate boots into high-impedence mode, with the power supply turned off. Let&rsquo;s select I2C, 100Khz (which is around the speed of the Raspberry Pi&rsquo;s I2C).

<pre>HiZ>m
1. HiZ
2. 1-WIRE
3. UART
4. I2C
5. SPI
6. 2WIRE
7. 3WIRE
8. LCD
9. DIO
x. exit(without change)

(1)>4
Set speed:
 1. ~5KHz
 2. ~50KHz
 3. ~100KHz
 4. ~400KHz
</pre>

I&rsquo;ve connected `3.3V` to `Vpu`, so we can safely turn on the PSU and enable the built-in pull-up resistors:

<pre>I2C>W
Power supplies ON
I2C>P
Pull-up resistors ON
</pre>

And search the available I2C address space:

<pre>I2C>(1)
Searching I2C address space. Found devices at:
0xA8(0x54 W)
</pre>

This bit confused me for ages. The [source code I had read][17] referred to 0x54 as the address, but the Bus Pirate wants to use the raw address for all writes, which is 0xA8. Writing to 0x54 just generates a lot of NACKs.

We want to write 0x0 0x1 to enable output:

<pre>I2C>[0xA8 0x0 0x1]
I2C START BIT
WRITE: 0xA8 ACK
WRITE: 0x00 ACK
WRITE: 0x01 ACK
I2C STOP BIT
</pre>

And enable all of the LEDs:

<pre>I2C>[0xA8 0x13 0xFF] [0xA8 0x14 0xFF] [0xA8 0x15 0xFF]
I2C START BIT
WRITE: 0xA8 ACK
WRITE: 0x13 ACK
WRITE: 0xFF ACK
I2C STOP BIT
I2C START BIT
WRITE: 0xA8 ACK
WRITE: 0x14 ACK
WRITE: 0xFF ACK
I2C STOP BIT
I2C START BIT
WRITE: 0xA8 ACK
WRITE: 0x15 ACK
WRITE: 0xFF ACK
I2C STOP BIT
</pre>

This picture from [Boeeerb&rsquo;s PiGlow Python library][18] is useful for addressing the LEDs:

![PiGlow Addressing][19]

Lets turn on a bright white by writing 0x0A 0xFF (LED number, intensity as an 8bit integer). Then we need to write 0x16 0x0 to flush the values.

<pre>I2C>[0xA8 0x0A 0xFF] [0xA8 0x16 0x0]
I2C START BIT
WRITE: 0xA8 ACK
WRITE: 0x0A ACK
WRITE: 0xFF ACK
I2C STOP BIT
I2C START BIT
WRITE: 0xA8 ACK
WRITE: 0x16 ACK
WRITE: 0x00 ACK
I2C STOP BIT
</pre>

And our first hint that any of this is really working, the `Hello World` of electronics: turning a light on:

![Hello, World][20]

 [1]: http://www.piday.org/
 [2]: http://www.urbandictionary.com/define.php?term=Steak%20and%20Blowjob%20Day
 [3]: http://dangerousprototypes.com/docs/Bus_Pirate
 [4]: https://insm.cf/=/024f5b5c.png
 [5]: https://code.google.com/p/the-bus-pirate/
 [6]: http://dangerousprototypes.com/2009/07/30/prototype-bus-pirate-3eeprom-explorer-board/
 [7]: http://shop.pimoroni.com/products/piglow
 [8]: https://insm.cf/=/8f8b11a0.png?inline=1
 [9]: http://www.si-en.com/uploadpdf/s2011517171720.pdf
 [10]: http://shop.pimoroni.com/products/adafruit-pi-t-cobbler-breakout-kit-for-raspberry-pi
 [11]: http://www.ebay.co.uk/itm/281209204268
 [12]: http://www.ebay.co.uk/itm/221397350202
 [13]: http://www.hobbytronics.co.uk/bus-pirate-cable
 [14]: https://insm.cf/=/038d7364.png
 [15]: http://crocketteng.com/blog/bus-pirate-pinout/
 [16]: https://insm.cf/=/028f0455.png
 [17]: https://github.com/pimoroni/piglow/blob/master/examples/piglow-example.py
 [18]: https://github.com/Boeeerb/PiGlow
 [19]: https://raw.github.com/Boeeerb/PiGlow/master/SN3218_addressing.jpg
 [20]: https://insm.cf/=/ac2a0456.png


