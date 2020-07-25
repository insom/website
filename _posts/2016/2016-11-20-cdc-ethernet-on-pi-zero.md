+++
date = "2016-11-20T16:00:00Z"
title = "Void Linux CDC Ethernet on the Raspberry Pi Zero"
type = "journal"
+++

A quick howto. [Void Linux][vl] is a minimal Linux distribution that
aggressively tracks upstream software with a rolling release model. They use
[runit][] as their `init` and have the option to use [musl][] as their `libc`.

[vl]: http://www.voidlinux.eu/
[musl]: https://www.musl-libc.org/
[runit]: http://smarden.org/runit/

Binaries are available for x86\_64 and ARM platforms, with a distribution
available for the Raspberry Pi 1 (which is close enough to the Zero).

Unfortunately, it looks like the default Pi build expects you to have a console
and keyboard on the machine. As I only have a serial terminal, the first thing
that I did was set it up to print console messages to the built-in UART, and
set up a getty on `/dev/ttyACM0`.

Follow the [installation instructions][inst], and while you have the filesystem
mounted, change `boot/cmdline.txt` to:

    root=/dev/mmcblk0p2 rw rootwait console=ttyAMA0,115200 kgdboc=ttyAMA0,115200 smsc95xx.turbo_mode=N dwc_otg.lpm_enable=0 loglevel=4 elevator=noop

[inst]: https://wiki.voidlinux.eu/Raspberry_Pi

That will take care of the boot messages. To be able to actually log in, we're
going to need to change to `etc/runsvdir/default` (relative to your
mount-point, `/mnt/rootfs` for me) and create a symbolic link to a file which
won't actually exist for you:

    ln -sf /etc/sv/agetty-ttyAMA0

That's going to make sure that a getty on ttyAMA0 loads on boot. This was
already included in the distribution, it just wasn't enabled by default.

---

The next step was enabling CDC Ethernet -- I think that this is one of the best
features of the Zero, you can have a little computer that you plug in with a
Micro USB lead and you can SSH straight to it.

To make the module load at boot time create the `modules-load.d` folder and
list the modules in the order that we need them (`dwc2` for gadget support,
`g_ether` for CDC Ethernet support)

    mkdir -p etc/modules-load.d
    tee etc/modules-load.d/ether.conf << EOF
    dwc2
    g_ether
    EOF

Because I like the device to always get the same DHCP lease and show up as the
same network device when plugged into my laptop, I also set the host and device
addresses:

    tee etc/modprobe.d/ether.conf << EOF
    options g_ether host_addr=32:70:05:18:ff:78 dev_addr=46:10:3a:b3:af:d9
    EOF

Finally, I make sure that the Zero will DHCP for this new network device the
first time that I plug it in:

    cd etc/sv
    cp -r dhcpcd-eth0 dhcpcd-usb0
    ex dhcpcd-usb0/run
    :%s/eth0/usb0/g
    :wq
    cd ../../etc/runit/runsvdir/default
    rm dhcpcd
    ln -sf /etc/sv/dhcpcd-usb0 # this absolute path won't exist yet

That's it for the Zero, just unmount the filesystems and pop the MicroSD card
into your Raspberry Pi.

---

I use Ubuntu on my laptop, so when I plugged in my Zero, it detected a new
network device. Select 'Edit Connections...' in the Network Manager applet to
reconfigure this new USB device that has shown up - you'll want to go to 'IPv4
Settings' and then choose 'Shared to other computers'. Okay your way out an
wait a few seconds for everything to catch up.

The IP address of your Zero should in `/var/lib/misc/dnsmasq.leases` -- SSH in
and enjoy!
