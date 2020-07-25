---
date: "2016-06-09T22:04:29Z"
title: "Pre-amp PCB design"
type: "journal"
layout: post
---

I'm sure I'm not the only person who does this:

I've built a project as a proof of concept. It worked fine, and now I'm
retrospectively writing it up for my blog. Unfortunately, I can see
improvements I could make, so as I'm writing it up I'm kind-of changing it
(well, *very* changing it).

![Schematic](/img/preamp/100percentcrop.png)

First off, I didn't really start with a schematic, I used some basic diagrams I
found of an example circuit for a non-inverting amplifier. I didn't use an
LM741, because I actually had a few LM348N's lying around. I haven't put that
in the schematic because it's a little embarrassing to waste a quad op-amp on a
single channel design.

![Actual Board](https://c1.staticflickr.com/2/1569/26212800840_a8668ac322_b.jpg)

(Witness my profligate waste of a quad op-amp!)

These fancy 3.5mm connectors on the schematic aren't the kind that I used -
I've put them in the schematic because the footprint was already in my KiCad
library and it would save me the job of adding a new parts library.

I was tempted to swap that 100K in R4 for a potentiometer, but now we're into
the realm of fantasy: that's a very different circuit than I actually built and
without building it an experimenting I'm not confident whether I should be
using a logarithmic or linear pot.

I'm probably going to finish this design off by actually laying out a PCB and -
because I can't help myself - probably getting it made. When I do that, I might
bring R4 out on a two pin connector so that it can be swapped out with other
resistances or pots. *That* is something I actually *have* done on the real
design:

![Pluggable Resistance](https://c3.staticflickr.com/2/1622/26212807250_693ac995aa_b.jpg)
