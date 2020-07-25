---
date: "2016-12-19T16:00:00Z"
title: "ESP8266 and MicroPython Temperature Logger"
type: "journal"
layout: post
---

My furnace is broken. Again.

I have internal temperature graphs that show what's going on, courtesy
of a BME280 Adafruit board that I bought:

![House Temperature](/img/temperature/housetemp.png)

You can see the slow build up to temperature, the rapid cycling at or
near the top of the cycle and when the furnace gives up and the
temperature creeps down. Oh, and by the way, it's pretty cold out.

Google reckoned it was down to -20 last night, but I honestly can't
get my brain around a temperature like that and I always feel it's
milder at my house than Google (or the Weather Channel) say it is.

It's time to science this up.

I had actually ordered another [BME280 board from eBay][eb] more than a
month ago, at the same time as the Adafruit order from [BuyAPi.ca][b], and
it just showed up yesterday. What perfect timing.

[eb]: http://www.ebay.ca/itm/Atmospheric-Pressure-Sensor-Temperature-Humidity-Sensor-Breakout-BME280-/272435211880
[b]: https://www.buyapi.ca/

I already had a couple of ESP8266 boards which had arrived with my
belongings from the UK, so I [followed the tutorial to compile and
install MicroPython on one][fo], grabbed [this great MicroPython library][th]
for the BME280 part and wired it all up.

[fo]: https://learn.adafruit.com/building-and-running-micropython-on-the-esp8266/build-firmware
[th]: https://github.com/catdog2/mpy_bme280_esp8266

I needed to use the WebREPL server to upload both the library and my
[new boot.py file which contains all of the Python][g] I had to write for
this. Basically it just sends a UDP packet to my Raspberry Pi every
few seconds.

There's a [tiny Ruby script on the Pi submitting the data][g] that it
receives into Graphite, and Grafana makes the pretty graphs.

[g]: https://gist.github.com/insom/b80b13f20cc7ff6ca992f540ed288be5

I used the Xiaomi battery pack I [blogged about before][b4] to power
the whole lot. As that previous post mentions, the battery pack will
turn off if there isn't enough current being drawn. Unfortunately the
ESP8266 and the BME280 are too damned power efficient, only drawing
73mA. This is less than the 90mA that we need.

![The Warm Unit](/img/temperature/IMG_20161219_210432.jpg)

I added the four-200&ohm; resistor pack, bringing the consumption
(according to my ammeter) to 170mA total. This is wasteful but, meh,
this is a quick hack. It also gives me a nice LED to see that the
power is on.

This is a useful feature because I threw the whole thing into a
transparent box to weather proof it, and now I can see if it's on or
not without going out into the cold.

![The Cold Unit](/img/temperature/IMG_20161218_220403.jpg)

Here's the completed graph:

![Outside Temperature](/img/temperature/outsidetemp.png)

You can see that it took a little while for the unit to get down to
outside temperature, it dropped to -18C at the lowest point, and the
battery ran for 16 hours.

The current consumption is (0.17A &times; 5.1V) 0.87W, so the power
should have run for ~18 hours, but given that it was -18C below, I
think it's fair to say that the battery did pretty well.

[b4]: https://insom.github.io/journal/2016/06/26/
