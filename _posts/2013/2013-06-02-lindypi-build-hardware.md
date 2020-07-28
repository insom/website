---
title: 'LindyPi Build- Hardware'
date: 2013-06-02
layout: post
---
[![][1]][2]

[View the full set][3]

Like many nerds, I have a server at home. It stays on around the clock and provides some basic services to my network: DNS, DLNA streaming, backup and somewhere to run the odd script or check a website from outside of the office network.

My server was a 2006-era Shuttle with a 60Gb laptop boot drive and a 1.5Tb Western Digital Green Edition drive.

[![][4]][5]

Nice as this was (and free, as it was ex-work and surplus to requirements) it had two major flaws: it&rsquo;s very loud (the fans on Shuttles are notorious) and it uses 80W of electricity. The server was in my Under-Stair-Data-Centre (USDC), and at night you could hear it through the stairs, which was a little unnerving. As per [Anthony Stanford-Clark][6], electricity costs (about) &pound;1 per Watt per year, so any replacement which cost less than that would pay for itself in the first year!

I knew that a Raspberry Pi plus some more parts I already had (or which were unwanted) would do the job just as well. In order to bring the same level of isolation between the jobs the server does I had to resort to fairly low-level software trickery, but I&rsquo;ll cover that in the next post.

I started with the chassis of a four-port SATA to USB external enclosure. The enclosure had failed for some undiagnosed reason (lights came on, it spoke USB, never showed any drives connected), so I couldn&rsquo;t reuse the controller board (which was have been really handy).

It _did_ still have a perfectly good and quiet power supply, which was capable of operating with the fan off, and had easily accessible 12V and 5V rails, as well as enough room inside for a Raspberry Pi and a 3.5&rdquo; HDD.

[![][7]][8]

Sadly, the first thing that I did turns out not to have been neccessary. I made a USB socket to [Molex 8981 connector][9], so that I could provide the 5V to the Pi&rsquo;s micro-USB port. For this I cut a USB extension lead in half, and soldered the red (5V) and black (ground) to pins 4 and 3 respectively of a Molex pass-through. This had originally been designed for a 12V fan, hence the cut-off red and black wires poking out of the top. Naturally, if you connected the USB to this, you would feed 12V to the Pi and probably let the magic smoke out of it, consigning it to the bin.

[<img src="https://farm6.staticflickr.com/5456/8829501918_9b9423d431_n.jpg" width="320" height="240" alt="lindypi-4" />][10] [<img src="https://farm3.staticflickr.com/2828/8829492634_62716aa8b7_n.jpg" width="320" height="240" alt="lindypi-6" />][11]

[<img src="https://farm8.staticflickr.com/7410/8829485838_c2ebd87322_n.jpg" width="320" height="240" alt="lindypi-7" />][12] [<img src="https://farm8.staticflickr.com/7416/8829481464_f5c380f1a7_n.jpg" width="320" height="240" alt="lindypi-8" />][13]

If I were doing this again, I would simply connect the 5V via the P1 header on the Pi, which has pins for 5V and ground at pins 2 and 6. A PC motherboard fan header is the same pitch the P1 of the Pi, so if you have a spare fan to sacrifice:

[<img src="https://farm8.staticflickr.com/7321/8928303895_541d32e50a.jpg" width="500" height="375" alt="better-pi-power" />][14]

(Adding to the colour confusion: if you re-use a PC motherboard fan connector, you need 5V on black and ground on yellow, leaving red unconnected. Please double and triple check this yourself, and don&rsquo;t blame me if you follow these instructions and melt your Pi.)

The PSU has an odd connector I&rsquo;ve not seen before, and I didn&rsquo;t have a male part, so I cut one of each of 5V, 12V and ground, and tucked the connector safely under the fan.

[<img src="https://farm8.staticflickr.com/7336/8829475798_a55d38279e_n.jpg" width="320" height="240" alt="lindypi-9" />][15] [<img src="https://farm8.staticflickr.com/7283/8829461764_38e5294f7e_n.jpg" width="320" height="240" alt="lindypi-12" />][16]

Now I needed to join the Molex Y cable (which has a very boring Molex to SATA power adaptor by this point), so I cut off a spare connector and use some terminal block.

[<img src="https://farm6.staticflickr.com/5321/8829472316_d51f7468e6_n.jpg" width="320" height="240" alt="lindypi-10" />][17] [<img src="https://farm6.staticflickr.com/5453/8829458820_2814021dec_n.jpg" width="320" height="240" alt="lindypi-13" />][18]

I put the USB to SATA adaptor, HDD, Raspberry Pi and all the leads in place, to check that there&rsquo;s really enough room:

[<img src="https://farm9.staticflickr.com/8544/8829451702_7e8e441813_n.jpg" width="320" height="240" alt="lindypi-15" />][19] [<img src="https://farm6.staticflickr.com/5450/8829436174_90f1e7e90c_n.jpg" width="320" height="240" alt="lindypi-18" />][20]

Just.

Now there were three bits of hardware work to give the build a proper finish. I&rsquo;m sad to admit I&rsquo;ve not adequately done any of these.

Wire the LEDs from the front panel up so they can be driven from GPIO:

[![][21]][22]

I worked out the pin outs, but didn&rsquo;t follow this through, because the server is sitting in the dark under my stairs.

Cut some nice mesh to cover the front of the enclosure:

[![][23]][24]

(Measure twice, cut once: this is too short). I have another piece for when I get around to the final thing I have not yet done.

Fitting a female RJ45 on the back of the case:

[![][25]][26]

At the moment, there&rsquo;s a 0.5m RJ45 patch lead poking out of a hole in the back. The right part is on order from eBay though, so I may get back around to this.

I&rsquo;m happy with my decision to leave the fan unconnected. latexmallard from Instructables is running a Pi in a reused case and has taken [some thermographic images][27], showing that with no cooling the Pi should operate 11C above the ambient temperature, which is abundantly safe. (He&rsquo;s also incorporated a UPS using a DC-DC convertor, so his Instructable is probably worth a read if you&rsquo;re interested).

Finally, here&rsquo;s a picture of the server in place, serving our streaming and backup needs. It only draws 15W and is saving us over &pound;60 a year. Though &pound;40 of year one just went on buying a Raspberry Pi and some metal mesh.

[<img src="https://farm9.staticflickr.com/8267/8829416492_32673a0fcc.jpg" width="500" height="375" alt="lindypi-24" />][28]

 [1]: https://farm6.staticflickr.com/5443/8829518870_df8958cfca_b.jpg
 [2]: https://www.flickr.com/photos/insomnike/8829518870/ "lindypi-2 by insomnike, on Flickr"
 [3]: https://www.flickr.com/photos/insomnike/sets/72157633688498850/
 [4]: https://farm8.staticflickr.com/7358/8928905212_b09b3a9670.jpg
 [5]: https://www.flickr.com/photos/insomnike/8928905212/ "shuttle by insomnike, on Flickr"
 [6]: http://stanford-clark.com/onepoundperwattperyear.html
 [7]: https://farm6.staticflickr.com/5327/8829525882_2e2e3bdd25.jpg
 [8]: https://www.flickr.com/photos/insomnike/8829525882/ "lindypi-1 by insomnike, on Flickr"
 [9]: http://en.wikipedia.org/wiki/Molex_connector
 [10]: https://www.flickr.com/photos/insomnike/8829501918/ "lindypi-4 by insomnike, on Flickr"
 [11]: https://www.flickr.com/photos/insomnike/8829492634/ "lindypi-6 by insomnike, on Flickr"
 [12]: https://www.flickr.com/photos/insomnike/8829485838/ "lindypi-7 by insomnike, on Flickr"
 [13]: https://www.flickr.com/photos/insomnike/8829481464/ "lindypi-8 by insomnike, on Flickr"
 [14]: https://www.flickr.com/photos/insomnike/8928303895/ "better-pi-power by insomnike, on Flickr"
 [15]: https://www.flickr.com/photos/insomnike/8829475798/ "lindypi-9 by insomnike, on Flickr"
 [16]: https://www.flickr.com/photos/insomnike/8829461764/ "lindypi-12 by insomnike, on Flickr"
 [17]: https://www.flickr.com/photos/insomnike/8829472316/ "lindypi-10 by insomnike, on Flickr"
 [18]: https://www.flickr.com/photos/insomnike/8829458820/ "lindypi-13 by insomnike, on Flickr"
 [19]: https://www.flickr.com/photos/insomnike/8829451702/ "lindypi-15 by insomnike, on Flickr"
 [20]: https://www.flickr.com/photos/insomnike/8829436174/ "lindypi-18 by insomnike, on Flickr"
 [21]: https://farm4.staticflickr.com/3804/8829432112_95f8e995d4.jpg
 [22]: https://www.flickr.com/photos/insomnike/8829432112/ "lindypi-20 by insomnike, on Flickr"
 [23]: https://farm6.staticflickr.com/5448/8829430498_f8fc506c6d.jpg
 [24]: https://www.flickr.com/photos/insomnike/8829430498/ "lindypi-22 by insomnike, on Flickr"
 [25]: https://farm4.staticflickr.com/3750/8928703335_ebc66241d4.jpg
 [26]: https://www.flickr.com/photos/insomnike/8928703335/ "panel mount by insomnike, on Flickr"
 [27]: http://www.instructables.com/id/Cheap-silent-and-efficent-Home-File-Server/step9/Did-it-work/
 [28]: https://www.flickr.com/photos/insomnike/8829416492/ "lindypi-24 by insomnike, on Flickr"


