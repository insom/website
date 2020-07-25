---
title: How I Backup
layout: post
date: 2014-07-23
url: /2014/07/how-i-backup/
categories:
  - Uncategorized
---
I _really_ hate losing things, and I am a little obsessive about my photos in particular. I&rsquo;m a pack-rat &#8211; I keep a lot of photos because they increase in value over time. That random test shot with a new camera shows how our house used to look (remember how the plaster was coming off that wall?) or a throwaway shot that&rsquo;s the only picture of one of the kids with _that_ haircut.

I&rsquo;m also still reeling from losing almost all of the photos of Jack from before he was two. There was a partition table incident on Helen&rsquo;s computer. Those photos were digital and are now gone. Friends came to our aid and sent us back photos that we had emailed them, but it&rsquo;s a tiny fraction of that two years.

So, that&rsquo;s _why_ I backup. This is how:

### iPhone Photos {#iphone-photos}

I run [BitTorrent Sync][1] on my iPhone and this syncs my camera roll with my desktop and [HP Microserver][2] at home and my Macbook at work &#8211; you need to remember to launch it in order to sync: it won&rsquo;t do it in the background (iOS won&rsquo;t let it). Assuming you can handle tapping on the icon every few days, you&rsquo;ll be covered. It&rsquo;s also the most convenient way to get your photos off your phone without a Lightning cable.

![BitTorrent Sync (on a Mac)][3]

I import these into [Lightroom][4], which I have decided to entrust with all of my photos. This means that there&rsquo;s now two copies on my desktop, on separate drives, and that iPhone photos enter into the flow that my &ldquo;proper&rdquo; camera photos have.

### Camera Photos {#camera-photos}

I do the usual things with [Lightroom][4]: I run the scheduled backups of the meta-data in case of massive corruption. Meta-data is data too, after all. This isn&rsquo;t that big a deal for me because I&rsquo;m not actually very organised and I rely on the EXIF data in the original files for most of the meta-data &#8211; and that is easily reconstructed if something terrible happens.

![Lightroom's Backup Dialog][5]

At the end of every month, I copy that month&rsquo;s folder out of [Lightroom][4] over to my [Microserver][2], where I import it into my [git-annex][6] repository.

[git-annex][6] gives you all the power of Haskell with the ease of use of git. (ha ha). What it actually does is really cleverly play to git&rsquo;s strengths for managing meta-data, like what a file is called, where it&rsquo;s stored and what its hash is, while filling in things it&rsquo;s not good at, like supporting large files, encryption and supporting things that don&rsquo;t have git installed.

### Git Annex {#git-annex}

Aside from photos, some other things which are large or that I want to keep go into [git-annex][6] &#8211; historical backups of my blog, email archives and my entire iTunes library are in there. I don&rsquo;t necessarily want all of these things on every computer that I own, but [git-annex][6] lets me be selective about which files I have on which computer.

If I need an MP3 from my iTunes library on my Macbook, for example, I can ask [git-annex][6] where it&rsquo;s stored and then ask it to connect to any of those places and get it for me. Once it&rsquo;s done, it&rsquo;ll update it&rsquo;s records to say that my Macbook _also_ has a copy.

![git-annex on OSX][7]

It will let me remove my local copy of files if I&rsquo;m low on space, but won&rsquo;t let me accidentally delete the last copy of my file (more accurately, it will let me specify a minimum number of copies that are in circulation &#8211; one is rarely enough for the paranoid).

(It has an interface only a mother could love, but there&rsquo;s a UI called [git-annex Assistant][8]. I prefer the control the CLI gives me).

My current [git-annex][6] remotes are:

  * `beta`: my Manchester virtual machine keeps most small data, but doesn&rsquo;t have the iTunes library, family videos or my photo collection.
  * `play`: my [Microserver][2] has a copy of absolutely everything.
  * `bob`: Bob the Server at work has a GPG encrypted copy of everything. It doesn&rsquo;t even run [git-annex][6] &#8211; it&rsquo;s an [rsync special remote][9].
  * `macbook`: my Macbook ebbs and flows, as it should. It&rsquo;s often where large assets (like edited video) are created &#8211; then I add them to [git-annex][6], make sure they are distributed around my remotes, and drop my local copy, giving me back SSD space. It has some, but not many, albums from iTunes.
  * `iwebftp`: I wrote an [iWeb FTP][10] special-remote &#8211; this was very, very easy and I happen to know that iWeb are keeping at least three copies of every file on iWeb FTP. This remote is encrypted, even though the transfer is encrypted and the data is stored encrypted at rest. Paranoia, right?

(If you&rsquo;re not keeping count, that means that _so far_ any photo I take is in seven places, eight if it&rsquo;s an iPhone photo).

### rsync from Manchester {#rsync-from-manchester}

`beta` is periodically backed up to my house. Nothing fancy.

### rsync on the Microserver {#rsync-on-the-microserver}

Everything on the [Microserver][2] is periodically backed up to other disks in the same server. Rather than RAID (which I don&rsquo;t need, as my SLA with my wife and kids is &ldquo;no nines&rdquo;), I use three disks in my [Microserver][2] as an original and two copies.

Everything good on the [Microserver][2] runs inside an [LXC container][11], which is stored in an LVM logical volume, and backed up from outside of the container. The minimal Debian install for the host runs off a USB pen and changes infrequently. I have a second USB pen with this install on it, in case the flash dies.

Because `beta` is downloaded to the [Microserver][2], it is now present on four disks total. Because `play` is a container on [Microserver][2], its [git-annex][6] install is also copied to another two disks. (10 copies of that iPhone photo, now).

### Windows {#windows}

For stuff that I don&rsquo;t even think to put into [git-annex][6], but that I&rsquo;d kick myself for losing, I back my `Users` and `Music` folders up on my desktop.

They go to an external [Western Digital MyBook][12] via the truly excellent [Bvckup 2][13]. Bvckup handles things like differential updates and bypassing file locking (with Volume Shadow Copies) while still being a beautiful application and not just porting `rsync` to Windows.

![Bvckup 2 Dialog][14]

While I have the space, I also back this up to a Samba share on `play`. You&rsquo;re probably getting the picture by now, but because that Samba share is on the [Microserver][2], it&rsquo;s going to a further two disks, too.

This backup includes the [BitTorrent Sync][1] folders and the [Lightroom][4] folders because &#8211; well, why not?

### OSX {#osx}

Finally, there&rsquo;s my Macbook. I really strive to keep everything important off of my Mac. All of my code lives in git, I push regularly, my documents are in [BitTorrent Sync][1] or Google Drive, my bookmarks are in the cloud and my email is in GMail. I&rsquo;m reasonably confident that if my Macbook took an unexpected bath, I would not lose more than a half-a-day&rsquo;s work.

![Carbon Copy Cloner][15]

But confidence isn&rsquo;t control, so I use Bombich Software&rsquo;s also-excellent [Carbon Copy Cloner][16] to create a bootable copy of my whole Macbook. I can plug this USB drive into a brand-new-in-box Mac and be up and running with my entire environment in minutes. It also covers me in case I suddenly realise I created an important file and just left it in my home folder.

_Needless to say_ this also includes another copy of my [BitTorrent Sync][1] folder and my [git-annex][6] remote for the Macbook.

### Downsides and Weaknesses {#downsides-and-weaknesses}

Nothing is perfect. I&rsquo;m happy with this backup situation, but it has some shortcomings and down sides.

  * If I _do_ want to purge a file, it&rsquo;s remarkably difficult to make sure I have gotten all of the copies. This hasn&rsquo;t really happened yet, but if you want a laugh at other people&rsquo;s expense you should read about [amateur pornographers not being able to delete shots from their Apple Photo Stream][17]. (&ldquo;I took a picture of my wife in lingerie and my in laws saw. Turning off the stream.&rdquo;).
  * There are several manual steps. I don&rsquo;t leave the [MyBook][12] connected to my PC (it&rsquo;s in a safe) &#8211; so I have to remember to do all of this. The [Lightroom][4] end-of-month copy to [git-annex][6] is the most annoying.
  * Despite there being up to 20 copies of some photos, they&rsquo;re actually only split among three real locations: home, work, Manchester. It&rsquo;s easy to be overconfident. Lower priority data only exists at home, though on several machines. It would be lost to a fire, for example.
  * Apart from the built-in delay of requiring manual steps, there&rsquo;s no provision for keeping historical copies. If you find out that you corrupted a file six months ago, you will not be able to get it back. You&rsquo;ll just have a dozen copies of the corrupted version.
  * Obviously, you require a lot of storage to keep all of these copies of things.
  * [BitTorrent Sync][1] and [Bvckup 2][13] are proprietary software. This is an issue for some people, and to a limited degree, it is for me. That said, I prefer a proprietary piece of software to a cloud service (_cough_ Dropbox), and [Bvckup][13] keeps my data in an open format (its original format, really), so I&rsquo;m okay with it.

 [1]: http://www.bittorrent.com/sync
 [2]: http://www.amazon.co.uk/gp/product/B00AHQUX86?ie=UTF8&camp=3194&creative=21330&creativeASIN=B00AHQUX86&linkCode=shr&tag=virtuvitri-21&qid=1406115978&sr=8-1&keywords=hp+microserver
 [3]: https://insom.iweb-storage.com/public/files/182bdd2b.png?inline=1
 [4]: http://www.amazon.co.uk/gp/product/B00CLD7Y4O?ie=UTF8&camp=3194&creative=21330&creativeASIN=B00CLD7Y4O&linkCode=shr&tag=virtuvitri-21&qid=1406115944&sr=8-1&keywords=lightroom+4
 [5]: https://insom.iweb-storage.com/public/files/blog-LR.png?inline=1
 [6]: https://git-annex.branchable.com/
 [7]: https://insom.iweb-storage.com/public/files/720105a3.png?inline=1
 [8]: http://git-annex.branchable.com/assistant/
 [9]: https://git-annex.branchable.com/special_remotes/rsync/
 [10]: https://www.iweb-ftp.co.uk/
 [11]: http://www.insom.me.uk/post/lindy-pi-2.html
 [12]: http://www.amazon.co.uk/gp/product/B00G28Y9BU?ie=UTF8&camp=3194&creative=21330&creativeASIN=B00G28Y9BU&linkCode=shr&tag=virtuvitri-21&qid=1406116072&sr=8-1&keywords=mybook
 [13]: http://bvckup2.com/
 [14]: https://insom.iweb-storage.com/public/files/blog-BVC.png?inline=1
 [15]: https://insom.iweb-storage.com/public/files/af2ddf49.png?inline=1
 [16]: http://www.bombich.com/index.html
 [17]: http://www.cultofmac.com/124235/how-to-delete-photos-from-iclouds-photo-stream/


