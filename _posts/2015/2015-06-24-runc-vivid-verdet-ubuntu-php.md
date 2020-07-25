---
title: 10 minutes with runc (getting PHP 5.6 on Ubuntu 12.04)
author: Aaron Brady
layout: post
date: 2015-06-24
url: /2015/06/runc-vivid-verdet-ubuntu-php/
categories:
  - Uncategorized
---
It&#8217;s [DockerCon season][1] and one of the announcements was [runc][2], the first deliverable from <del datetime="2015-06-24T08:32:05+00:00">Omni Consumer Products</del> the [Open Container Project][3].

It&#8217;s underdocumented, so I had a play with it, and here&#8217;s a dump of how to get an [Ubuntu Vivid Verdet][4] running, with PHP and a document root exposed from the outside. This is enough to use a newer PHP version while keeping your machine on an LTS (even on the previous LTS, as I was doing thing on a 12.04 VM in Canada).

Get and build [runc][2]. You will need a [go][5] installation, and I found the instructions for runc weren&#8217;t quite enough, here&#8217;s what I did:

    git clone https://github.com/opencontainers/runc.git
    cd runc
    go get github.com/tools/godep
    godep get # I needed this. It errors, but that's okay/
    make
    

So, you should have a runc binary now, verify with `./runc -help`. Also, runc really likes to either be on the path or be called with an absolute path. Assuming you don&#8217;t want to install it, from here on in I&#8217;ll call it absolutely.

Next up: we need an Ubuntu environment with PHP and Apache. We can use [debootstrap][6](8) for this:

    sudo /usr/sbin/debootstrap --variant=minbase --include=libapache2-mod-php5 \
    --no-check-gpg --no-check-certificate vivid /vivid
    

And then we&#8217;ll need a script to run as PID 1. If we&#8217;re not using an init, something like this will do:

    #!/bin/sh
    . /etc/apache2/envvars
    exec apache2 -DFOREGROUND
    

I&#8217;ll call it `doit.sh` and put it in the root of the new Ubuntu environment, so `/vivid/doit.sh`.

We&#8217;ll need a `container.json` file. This isn&#8217;t documented yet, as far as I can see, but perusing the source and playing got me [this gist][7]:



This is mostly like the example, except I&#8217;ve chosen not to use a `network` or `uts` namespace (I&#8217;m happy for it to share with my VM), and I&#8217;ve added the `DAC_OVERRIDE` capability &#8211; this is what lets root open files it doesn&#8217;t own, and the Ubuntu packaged Apache requires it. I&#8217;ve also created a bind mount from `/var/www/html` within the container to `/www` on my host VM. This needs to exist, and I&#8217;ll put a basic `index.php` in, too:

    <?php phpinfo();
    

&#8230; and that&#8217;s it! Let&#8217;s run it:

    sudo `pwd`/runc
    

If you don&#8217;t already have a web server running on port 80 of your host, you can now visit your hosts IP and see the PHP info page, being served from your new container:

![phpinfo][8]

If you want to make it work on boot, an upstart job like this will do it:

    start on local-filesystems
    stop on deconfiguring-networking
    respawn
    chdir /home/aaron/Repo/runc
    exec /home/aaron/Repo/runc/runc
    

I&#8217;ll post more as I learn more.

 [1]: http://www.dockercon.com/
 [2]: https://github.com/opencontainers/runc
 [3]: https://www.opencontainers.org/
 [4]: http://releases.ubuntu.com/15.04/
 [5]: http://golang.org
 [6]: https://wiki.debian.org/Debootstrap
 [7]: https://gist.github.com/f0f50e952b52b7354ec6.git
 [8]: https://insom.iweb-storage.com/public/files/a5b7a88d.png?inline=1


