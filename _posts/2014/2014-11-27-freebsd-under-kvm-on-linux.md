---
title: FreeBSD under KVM on Linux
layout: post
date: 2014-11-27
---
The incantation that you will need to get up and running:

> kvm -display curses -m 512 -cpu kvm64 -boot d \

> -cdrom /mnt/scratch/FreeBSD-10.1-RELEASE-amd64-bootonly.iso \

> -enable-kvm -net tap -net nic,model=virtio -hda /dev/1P5T/bsd

This is after grabbing the FreeBSD 10.1 ISO and putting it in `/mnt/scratch`, and after using lvm to create a 10Gb raw device for FreeBSD, with `lvcreate -n bsd -L 10G 1P5T` (my volume group is, accordingly, 1P5T).

The `-display curses` flag will give you a full screen curses interface as long as the guest VM stays in text mode (which the FreeBSD installer will), allowing you to complete the initial installation.

FreeBSD 10.1 supports VirtIO so that there&#8217;s no need to emulate another network card. I added the newly created `tap0` device to my bridge after starting KVM with `brctl addif br1 tap0`. I run DHCP on my network, so all of the right things happened.

Once I had finished the install (and enabled SSH) I was able to use the even simpler line of:

> kvm -display none -m 512 -cpu kvm64 \

> -enable-kvm -net tap -net nic,model=virtio -hda /dev/1P5T/bsd

Enjoy FreeBSD.


