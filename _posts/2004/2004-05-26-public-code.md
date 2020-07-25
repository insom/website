---
title: Writing Public Code
date: 2004-05-26
---

When writing code "for public consumption" or even just for display, I dislike releasing proof-of-concept code. Sure, I have 10 minute hacks in my snippets section, but what about the longer pieces that aren't polished, but are still good?

I have two specific pieces of code: one which takes an image as a parameter and creates a thumbnail of it with a pretty border gleaned from another image, and one which decodes barcodes from images.

Both of these pieces of code are conceivably useful to someone, but they are full of unexplained (magic) constants, bad variable names that put typing speed above readability, hardcoded defaults, and are almost totally void of comments.

It pains me to release them, but I haven't posted anything substantial in months, and most of it comes from the fact that even when I get time to write some code, I rarely have time to polish to the level that I consider fit for public consumption.

Without further ado, I give you [Python Snippets: Decoding Barcodes & Framing Thumbnails.][partial]

[partial]: /hacks/partial.html