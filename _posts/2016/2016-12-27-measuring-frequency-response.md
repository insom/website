---
date: "2016-12-27T16:00:00Z"
title: "Measuring Frequency Response"
type: "journal"
layout: post
---

In my short electronics career, I've built headphone and power
amplifiers, including a valve amp, and a microphone pre-amp of [my own
(extremely simple) design][own]. I've modified others, too.

[own]: /journal/2016/06/09/

I like the sounds of these devices to a greater or lesser degree, possibly for
pretty unscientific reasons.

One thing I've wanted to do for a while is stick some science on it and
actually measure their frequency responses.

I recently had a good excuse because I found my microphone pre-amp and I was
going to rebuild it properly and put it in a box but I _also_ found this [SSM2019
chip][ssm] that I'd received a sample of from Analog.

The SSM2019 is effectively a pre-amp on a chip, only requiring power, signal
and a 10K variable resistor to control gain. Its [datasheet][ds] promises a
flat frequency response past 20KHz, which is about as good as [human hearing
range][hhr]

[ds]: http://www.analog.com/media/en/technical-documentation/data-sheets/SSM2019.pdf
[ssm]: http://www.analog.com/en/products/audio-video/audio-amplifiers/micpre-amp-audio-products/ssm2019.html
[hhr]: https://en.wikipedia.org/wiki/Hearing_range

There was no point in rebuilding my basic LM348N-based amp if the SSM was
going to be better and even simpler.

Curiously, the LM348N [doesn't list frequency response][nofr] on its datasheet
(as available from Digikey). I found a [Fairchild version on a Russian
website][fc] which suggests it falls off well before 10KHz.

[fc]: http://eicom.ru/pdf/datasheet/Fairchild_PDFs/LM348-248/LM348-248.html
[nofr]: http://www.digikey.com/product-detail/en/texas-instruments/LM348N/296-12849-5-ND/476163

---

As a happy coincidence, Hackaday recently ran an article called ["Controlling
Your Instruments From A Computer: Doing Something Useful"][hd]. In it, Jenny
List measured a filter she designed against the simulation (and found the real
one wanting). She used a Rigol oscilloscope for the readings and a Raspberry Pi
as a signal generator. I have both of those! This was all going to be a walk in
the park!

Nope.

I checked out her fork of [freq\_pi][pf] and used the Rigol to verify that
GPIO4 on the Pi was outputing some very stable square waves. Then I found
it's only [capable of generating waves from 61KHz to 250Mhz][c]. (Well, I say
_only_. That's incredibly useful, just not for me).

[c]: https://github.com/JennyList/LanguageSpy/blob/master/RaspberryPi/rf/freq_pi/freq_pi.c#L823

It was time to completely switch tack.

[pf]: https://github.com/JennyList/LanguageSpy/tree/master/RaspberryPi/rf/freq_pi
[hd]: https://hackaday.com/2016/11/29/controlling-your-instruments-from-a-computer-doing-something-useful/

---

Last Christmas I was given an [Analog Devices ADALM1000][1k]. This is a
combination two channel signal generator / oscilloscope aimed at the
educational market.

The basic idea is that you build some filters or op-amp designs and have one
channel generate a signal, and then measure it with the other channel.

That sounds great for testing an amplifier too, and it's capable of generating
a sine-wave from 1Hz to 20KHz, so it perfectly matches the range I'd like to
test.

[1k]: https://wiki.analog.com/university/tools/m1k

![Desk](/img/freq/desk.jpg)

This is everything held together with crocodile clips. This photo actually
shows me testing my [NP100v12][va] valve amp, but the basic set up is the
same.

[va]: http://diyaudioprojects.com/Solid/12AU7-IRF510-LM317-Headamp/

I connected channel A to the ground and input of the pre-amp and channel B to
ground and output. I powered the amp from a 9V battery to avoid introducting
any mains hum.

![Scope](/img/freq/scope.png)

This is the Alice software for the ADALM1000. It's all written in
Python and pretty hackable. It's not as polished as the Pixelpulse
software which is also available from Analog, but once you get used to
it this software is far easier to control accurately.

In this screen shot I've set channel A to be AWG (arbitrary waveform
generator). The shape is sine (you can't see that, it's hidden under the
`shape` menu). Input amplitude is from 0 to 0.1V, and we're generating a 100Hz
wave as a test.

Channel B is measuring voltage. It's set to display the waveform as
well as the peak voltage (V<sup>max</sup> -- 1.01V here). Our gain (G)
here is 10.

By changing the frequency I created a table of Hz vs. V<sup>max</sup>:


<table border="1">
<tr><th>Hz</th><th>V<sup>max</sup></th></tr>
<tr><td>10 </td><td> 1.03</td></tr>
<tr><td>50 </td><td> 1.03</td></tr>
<tr><td>100 </td><td> 1.01</td></tr>
<tr><td>500 </td><td>  1.005</td></tr>
<tr><td>1000 </td><td> 1.015</td></tr>
<tr><td>2500 </td><td> 1.00</td></tr>
<tr><td>5000 </td><td> 0.98</td></tr>
<tr><td>10000 </td><td> 0.92</td></tr>
<tr><td>15000 </td><td> 0.84</td></tr>
<tr><td>20000 </td><td> 0.75</td></tr>
</table>

This isn't very clear, although even I can see the drop-off starting after 5000Hz.

[A little Python script][pl] to generate a plot will help with visualising what this means.

[pl]: https://gist.github.com/insom/46af7810b0b4d344659e6f6984d80ffc

![Plot](/img/freq/plot.png)

Oh.

Expect a follow up when I build the SSM2019 based pre-amp, I guess.
