---
title: Moar Aaron
layout: post
date: 2013-08-07
---
My short post on [Responsive Designs vs. Traditional Builds][1] is up on $WORK&rsquo;s blog. While I&rsquo;m not a designer, playing with this stuff has been fun. Responsive web design makes CSS almost programmerish by adding what is essentially a `if` statement to the language.

<strike>You can follow me (and this blog, which auto-posts using Pour-Over) on pay-to-play microblogging site App.net. If you use this link to create an account, you&rsquo;ll automatically follow me and I&rsquo;ll get a small amount of extra space on the service.</strike><br>

(I also worked on a screenshot-tastic post for iWeb FTP for people [getting started with the service][6] that probably isn&rsquo;t of too much interest to this audience, but consider it linked-to.)

[<img src="https://farm4.staticflickr.com/3823/9460173470_faf9314e00_c.jpg" width="800" height="600" alt="Untitled" />][7]

I&rsquo;ve got a new [bottom bracket][8] waiting for me at home. My old one, well, it&rsquo;s a little rusty.

[<img src="https://farm8.staticflickr.com/7429/9457390801_99539c684b_c.jpg" width="800" height="600" alt="Untitled" />][9]

_And_ I dumped quite a lot of time into getting quieter cooling on my ProLiant ML115 G5. I use this server-grade hardware as a gaming PC, and I&rsquo;m kind of picky about noise.

I replaced the stock 92mm with this [Arctic Cooling F9 PWM controlled one][10] (amazon affiliate link) because there&rsquo;s a four-pin header on the board. Unfortunately, as part of the [POST process][11] process the HP decides to slow the fan down, and then immediately panics about the RPMs going below 1900. Once it does that, it powers off.

I spent some time playing with it and even resolved to use a small microcontroller to &ldquo;fake&rdquo; 1900RPM to the sense pin, but in the end just leaving the fourth pin disconnected (pictured) keeps the fan spinning fast enough and it&rsquo;s quieter than the stock fan even when it stays at 100% all of the time. I butchered the old fan&rsquo;s cable to do this and then used heat-shrink to make everything look un-butchered.

I may revisit this, for kicks. I even got to break out my oscilloscope while trying to get everything to work.

 [1]: http://www.iwebsolutions.co.uk/blog/responsive-designs-vs-traditional-builds/
 [6]: http://blog.iweb-ftp.co.uk/features/getting-started-with-iweb-ftp/
 [7]: https://www.flickr.com/photos/insomnike/9460173470/ "Untitled by insomnike, on Flickr"
 [8]: https://en.wikipedia.org/wiki/Bottom_bracket
 [9]: https://www.flickr.com/photos/insomnike/9457390801/ "Untitled by insomnike, on Flickr"
 [10]: http://www.amazon.co.uk/gp/product/B002G3CN22/ref=as_li_ss_tl?ie=UTF8&camp=1634&creative=19450&creativeASIN=B002G3CN22&linkCode=as2&tag=virtuvitri-21
 [11]: http://en.wikipedia.org/wiki/Power-on_self-test
