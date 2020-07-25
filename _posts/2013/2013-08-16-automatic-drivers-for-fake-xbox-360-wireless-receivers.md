---
title: Automatic Drivers for Fake Xbox 360 Wireless Receivers
layout: post
date: 2013-08-16
url: /2013/08/automatic-drivers-for-fake-xbox-360-wireless-receivers/
categories:
  - Uncategorized
---
I bought a cheap Xbox 360 Wireless Receiver from eBay so I could re-use the wireless pads I have (which also happen to be the best controllers I&rsquo;ve ever used) with my new PC gaming set up.

The one I ended up with seems a fairly common Chinese import and came with a driver CD (of 32bit drivers) and a very small set of instructions (which didn&rsquo;t work). Looking at the driver CD it was clear that they were an altered version of the official Microsoft drivers, which suggested that they would be very compatible [with the official Microsoft Windows 7 64-bit drivers][1].

I installed the drivers (I agree, next, next, next) but they didn&rsquo;t recognise the adaptor, and I still had an &ldquo;Unknown Device&rdquo; under &ldquo;Other devices&rdquo; in `Device Manager`.

Find the device, and select `Update Driver Software`:

![][2]

![][3]

![][4]

![][5]

![][6]

Click `Yes` here, because we know what we&rsquo;re doing, right?

![][7]

All of those steps brought the adaptor to life, and I could pair a controller with it and all of the right things happened. After a reboot however, I had to go through all of the installation steps again- it didn&rsquo;t take too many repetitions before I decided to do something about it.

### Editing Windows .INF files for Fun <strike>and Profit</strike> {#editing-windows-inf-files-for-fun-wzxhzdk1and-profitwzxhzdk2}

First, a quick introduction to how Windows pairs up devices and device drivers:

Both USB and PCI busses identify devices by two 16 bit numbers, a vendor ID and a product ID. These are normally displayed as four hexdecimal characters for each number, and you might even see them in the boot-up sequence on some older computers (Intel famously have 8086, which is just rad, as that&rsquo;s the CPU family that made them rich).

You can view this by clicking on a device&rsquo;s properties in `Device Manager` and viewing the `Hardware Ids` (sic) property. In this case, they are `045E` and `0291`, respectively.

![][8]

It should be noted that `045E` is actually Microsoft Corporation, and that this Far-Eastern knock-off is seriously breaking the rules by re-using another company&rsquo;s identifier. `0291` is _not_ the ID of the official receiver, though, which is why the device doesn&rsquo;t _just work_. The real device is `0719`. I don&rsquo;t understand why they have done this: if you&rsquo;re going to clone a device&rsquo;s USB identifier, you should probably clone both.

There&rsquo;s a copy of the Xbox driver files in `C:\Program Files\Microsoft Xbox 360
Accessories` &#8211; the file we&rsquo;re going to change now is `Xusb21.INF`. This file lists the installation instructions for the wired and wireless controllers, as well as the play & charge cable. I can&rsquo;t reproduce the whole thing, because of copyright, but excerpting some should be okay:

<div class="codehilite">
  <pre><span class="c1">; Copyright 2006-2007 Microsoft Corporation</span>
<span class="c1">;</span>
<span class="c1">; XUSB21.INF file</span>
<span class="c1">;</span>
<span class="c1">; Installs the XUSB21 device driver</span>
<span class="c1">;</span>
<span class="c1">; Supports the following devices</span>
<span class="c1">; Wired Common Controller    USB\Vid_045E&Pid_028E</span>
<span class="c1">; Wireless Common Controller USB\Vid_045E&Pid_0719</span>
<span class="c1">; Wired CC Compatible        USB\MS_COMP_XUSB10</span>
<span class="c1">; Wireless CC Compatible     USB\MS_COMP_XUSB20</span>
<span class="c1">;</span>
<span class="c1">; Installs a NULL Service for the Play and Charge Cable</span>
<span class="c1">; Play and Charge Cable      USB\Vid_045E&Pid_028F</span>
</pre>
</div>

Hey, there&rsquo;s that 0719 we were looking for. All we need to do is search and replace across the whole file, changing 0719 to 0291. As a cheeky nod to the knock-off I&rsquo;m using, I also changed the `XUSB21.DeviceName` line, which dictates what shows up in `Device Manager`:

![][9]

The very next time you need to manually update the drivers for this device, point it at the above folder and it will autodetect your device. It will also install it into the `Windows DriverStore` so you won&rsquo;t be prompted again. (The first time, though, you will be asked if you&rsquo;re okay installing an unsigned driver- tampering with the .INF file invalidates the digital signature).

I hope the above was useful. If you have any comments, please let me know via Twitter ([@insom][10]) or App.net ([@insom][11]).

 [1]: http://www.microsoft.com/hardware/en-us/d/xbox-360-wireless-controller-for-windows
 [2]: https://f.insom.me.uk/blog-images/xbox/Unknown%20Device%201.png
 [3]: https://f.insom.me.uk/blog-images/xbox/Update%20Driver%201.png
 [4]: https://f.insom.me.uk/blog-images/xbox/Update%20Driver%202.png
 [5]: https://f.insom.me.uk/blog-images/xbox/Update%20Driver%203.png
 [6]: https://f.insom.me.uk/blog-images/xbox/Update%20Driver%204.png
 [7]: https://f.insom.me.uk/blog-images/xbox/Update%20Driver%205.png
 [8]: https://f.insom.me.uk/blog-images/xbox/Hardware%20IDs.png
 [9]: https://f.insom.me.uk/blog-images/xbox/Fake%20Xbox%20360%20Image.png
 [10]: https://twitter.com/insom
 [11]: https://alpha.app.net/insom


