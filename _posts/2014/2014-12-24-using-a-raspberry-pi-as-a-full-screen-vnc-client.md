---
title: Using a Raspberry Pi as a full-screen VNC client
author: Aaron Brady
layout: post
date: 2014-12-24
url: /2014/12/using-a-raspberry-pi-as-a-full-screen-vnc-client/
categories:
  - Uncategorized
---
Just the facts:

Follow [the installation instructions][1] from another Linux machine. It appears you have to bootstrap from Linux, unless I&#8217;m missing an SD card image somewhere.

It&#8217;ll DHCP, and you can SSH in with `root` & `root`.

Install VNC, X, dwm and xdotool:

    pacman -Sy tigervnc xf86-input-evdev xf86-video-fbdev xorg-server xdotool dwm
    

Tweak your /boot/config.txt [according to the wiki][2] (I just disabled overscan, YMMV).

Use `vncpasswd` to store the password for your VNC _server_ (as root, in my case).

Then create `/root/start-x-session` with these contents:

    #!/bin/bash
    sleep 10
    export DISPLAY=:0
    X :0 & sleep 2
    dwm & sleep 2
    xdotool key Alt+b
    xdotool mousemove 2000 2000
    xset s reset
    xset s off
    xset -dpms
    while true; do
      vncviewer -passwd /root/.vnc/passwd Shared=1 ViewOnly=1 FullScreen=1 your.vnc.server.here
      sleep 2
    done
    

And this systemd unit in `/etc/systemd/system/vnc.service`:

    [Unit]
    Description=VNC Viewer
    After=network.target
    
    [Service]
    Type=oneshot
    RemainAfterExit=yes
    ExecStart=/root/start-x-session
    ExecStop=/bin/true
    
    [Install]
    WantedBy=multi-user.target
    

Enable it with `systemctl enable vnc.service` and reboot!

 [1]: http://archlinuxarm.org/platforms/armv6/raspberry-pi
 [2]: http://elinux.org/RPiconfig


