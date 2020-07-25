---
date: "2016-03-24T23:25:04Z"
title: "Contribution streak: Arduino RAM dumper and Sensu Plugins"
type: "journal"
layout: post
---

Clearly I didn't do any more Laravel yesterday, after securing my square for
Java. Oh, well.

I did some work on a [new repository][nr] - it bundles up the latest version
of my Arduino RAM programmer &hellip; thing and some `Makefile`s for building
raw binaries from C and assembly.

The programmer / monitor supports four commands: (z)ero the RAM, (l)oad the
default program, (d)ump the RAM to the serial port and p(o)ke a byte of RAM.

Today I added a utility which converts binary files into a format which can be
poked over the serial port, so it's possible to load new programs into the RAM
without reflashing the Arduino (which is what I've been doing so far).

I'll write this up in an entry under the Z80 project, but I'm pretty pleased
with it, it's following the pattern or writing terrible code in the heat of
the moment in the Arduino IDE, and then fixing it up in a real editor later in
the day.

In other news, my [Sensu Gearman plugin][sgp] is now officially part of the
[sensu-plugins.io organisation][so], thanks to a helping hand from
[@eheydrick][eh] on GitHub / Freenode!

Tomorrow is a bank holiday, it would be good to get back to some Laravel, but
I've also taken my Z80 home with me for the long weekend. I'd like to flesh
out that project on here. With some luck I can do both.

[nr]: https://github.com/insom/LittleComputer
[sgp]: https://github.com/sensu-plugins/sensu-plugins-gearman
[so]: https://github.com/sensu-plugins
[eh]: https://github.com/eheydrick
