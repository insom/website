+++
date = "2017-04-02T22:00:00Z"
title = "Making your own private Internet"
type = "journal"
+++

*blows dust off blog*

It's not that I haven't been busy! I've built [and upgraded][ug], and broken, a
CNC mill. [I've converted a 70's toy to accept WiFi and speak Python][bigtrak].
I even converted another PS2 keyboard to USB .. [kinda][]. I just haven't
written any of it up on my blog.

I knew I had to write up the even _older_ stuff about FPGAs etc., and I think
that was holding me back.

This is not that post.

This is a post about using [WireGuard][wg], [VXLANs][vxlans] and Linux bridge
devices to make your own private network between hosts that can neccessarily
all talk to each other.

---

The [WireGuard quickstart][qs] is pretty comprehensive, so I'm not going to
duplicate it here. For my part, I have five machines:

 Machine | Location
---------|--------------
 rho     | Paris, FR
 epsilon | Eastern US
 vorke   | Ottawa, CA
 bob     | Stafford, UK
 pi0     | Roaming

Rho, Epsilon and Bob have static IP addresses and are reachable from the
outside. Vorke has a dynamic IP address which is reachable from the outside.
Pi0 could be anywhere, has a dynamic IP and is usually behind NAT.

I checked out the WireGuard source and built the kernel module. Because I'm a
lesson to others, I am using a mix of `x86`, `amd64` and `armel`. I'm also
using a mix of Debian, Ubuntu and VoidLinux, and my Paris machine is a Marvell
Armada SoC. Don't be like me.

Let's assume that

    cd WireGuard/src ; make ; sudo make install

does the right things for you. You'll have a `wg` utility on your path, a new
kernel module in the directory that matches your running kernel and an
`/etc/wireguard` directory, waiting for a config.

I changed to `/etc/wireguard` on each machine and generated my keys:

    wg genkey | tee privatekey | wg pubkey > publickey

Then I assigned `10.88.88.0/24` out of thin air. (It's in an RFC1918 network,
so this is fine. Anything starting with `10.` is fair game as long as no other
network you are connected to is using it).

Each machine has a config which lists the other nodes in it:

	# Rho
	[Interface]
	PrivateKey = REDACTED
	ListenPort = 56560

	# Bob
	[Peer]
	PublicKey  = REDACTED
	AllowedIPs = 10.88.88.1/32
	Endpoint   = 86.188.161.69:56560

	# Epsilon
	[Peer]
	PublicKey  = REDACTED
	AllowedIPs = 10.88.88.4/32
	Endpoint = 104.196.99.86:56560

	# Vorke
	[Peer]
	PublicKey  = REDACTED
	AllowedIPs = 10.88.88.3/32

	# Pi0
	[Peer]
	PublicKey  = REDACTED
	AllowedIPs = 10.88.88.5/32

You don't have to always list every node in the config, only the other nodes
that you expect that machine will talk to. For example, I've only put `Pi0` in
`Rho`'s config, because those two machines only talk to each other via WireGuard.

You'll notice that `Endpoint` is only filled in for machines which are
publically reachable on a static IP. The other machines will initiate a
connection _out_ to the static ones. Once that happens, the static ones know to
use that existing UDP socket pair to talk back to them.

I create and configure the WireGuard network interfaces on every machine:

	modprobe ipv6
	modprobe udp_tunnel
	modprobe ip6_udp_tunnel
	ip link add dev wg0 type wireguard
	wg setconf wg0 /etc/wireguard/config
	ip link set up dev wg0
    ip addr add 10.88.88.4/24 dev wg0 # pick a unique IP for each machine

You can verify that everything is working now by pinging from place to place.
If you're okay with the `wg` kernel module making routing decisions for you,
and having to have all nodes be able to talk to all other nodes, you could stop
now.

---

I wasn't happy with this, and I also wanted to deal with the issue of MTU. On
_my_ network, the `wg0` device has an MTU of 1420. This _should_ be fine,
because we have path-MTU discovery, but we live in crappy times and between
overzealous filtering of ICMP, refusal to route fragmented packets and anycast
IPs that do the wrong thing, this will cause problems at some point.

My solution for this is to run [VXLANs][vxlans] over the encrypted
point-to-point tunnels that WireGuard have given us. They are effectively VLANs
which are implemented in UDP instead of at layer 2.

These act more like regular network devices, their routing (and switching)
decisions work in standard ways, and I can tell the kernel to make the devices
have 1500-byte MTUs and just send fragmented packets over WireGuard. It won't
neccessarily be efficient, but it will work.

Each of these VXLANs is going to form a point to point network of their own. I
like to think of them as "virtual wires". Or cloud Ethernet. Or something.
Given a bunch of virtual wires which connect between each other but don't form
a complete mesh, I thought of a few ways to make this work:

* Static routing over the IPs. I don't have a _lot_ of hosts, but I have enough
  for this to become annoying, and it wouldn't provide any form of redundancy.
* Use a dynamic routing protocol (like BGP). Because the hosts don't form a
  full mesh, they couldn't live inside the same autonomous system, but I could
  allocate a bunch of ASes from the test range (64512 and above).  
  &nbsp;  
  This could be cool because I could join my BGP based Calico network in. It
  does mean configuring some routing software (probably Quagga). I may still
  revisit this, but it wasn't what I chose to do.
* Solve this at layer 2 by using Linux bridges and the [spanning tree protocol][stp].

---

Spanning tree will mean that I really can just treat these VXLANs like cables
-- connect them all to a core switch, connect them to each other, and let STP
avoid switching loops.

In real network gear, if you have two connections between `Switch A` and
`Switch B`, you would cause a switching loop -- packets going to `Switch B`
from `A` would end up going _back_ to `A` and then back to `B` and bad, bad
things would start to happen.

To avoid this, when a layer 1 connection comes up on an STP enabled switch it
sends some broadcast packets called BPDUs. If it receives that packet back on
another interface, it will disable one of the two interfaces to avoid a loop.
No real traffic can flow until this process has run its course, which takes
around 30 seconds.

Apart from avoiding pain when connecting network equipment together, STP also
gives you a layer of redundancy -- if the active port stops sending packets,
your switch can attempt to bring the port which was disconnected ('Blocked' in
STP speak) into to use ('Forwarding').

This is going to be great for my internetwork, because if one of the nodes is
unavailable then all of the rest of the nodes which have cross connects will
eventually notice and reconfigure themselves into a mostly working network.

Because it doesn't require every node to talk to every other, connections like
Pi0 -- which only has one upstream connection, are treated just like an access
port on a switch. They have no redundancy, but they are considered down-stream
of which every Linux bridge they are connected to.

```
brctl addbr internet
brctl stp internet on
case $(uname -n) in
epsilon)
    ip addr add 10.99.99.4/24 dev internet
    ip link add vorke   type vxlan remote 10.88.88.3 id 1 dstport 4789
    ip link add bob     type vxlan remote 10.88.88.1 id 2 dstport 4789
    ip link add rho     type vxlan remote 10.88.88.2 id 4 dstport 4789
;;
vorke)
    ip addr add 10.99.99.3/24 dev internet
    ip link add bob     type vxlan remote 10.88.88.1 id 3 dstport 4789
    ip link add epsilon type vxlan remote 10.88.88.4 id 1 dstport 4789
    ip link add rho     type vxlan remote 10.88.88.2 id 5 dstport 4789
;;
sudo ip link set up dev internet
for i in epsilon bob vorke rho pi0; do
    ip link set up $i
    brctl addif internet $i
    ethtool -K $i tx off
done
```

The above establishes VXLANs between the different hosts (only two are
included, for brevity), adds them to an STP enabled bridge and configures IPs
on the bridge devices.

Because of a bug ... somewhere (I suspect WireGuard) I had to disable hardware
accelerated tx checksums, that's what the `ethtool` line is doing.

---

### Epilogue

We can view the status of things with `brctl showstp internet`:

```
EPSILON:~$ sudo brctl showstp internet
internet
 bridge id              8000.5299c5e0d97b
 designated root        8000.16500a8e632a
 root port                 1                    path cost                100
 max age                  20.00                 bridge max age            20.00
 hello time                2.00                 bridge hello time          2.00
 forward delay            15.00                 bridge forward delay      15.00
 ageing time             300.00
 hello timer               0.00                 tcn timer                  0.00
 topology change timer     0.00                 gc timer                 276.72
 flags


bob (1)
 port id                8001                    state                forwarding
 designated root        8000.16500a8e632a       path cost                100
 designated bridge      8000.16500a8e632a       message age timer         19.86
 designated port        8002                    forward delay timer        0.00
 designated cost           0                    hold timer                 0.00
 flags

rho (3)
 port id                8003                    state                  blocking
 designated root        8000.16500a8e632a       path cost                100
 designated bridge      8000.3a3bee4c8584       message age timer         19.87
 designated port        8002                    forward delay timer        0.00
 designated cost         100                    hold timer                 0.00
 flags

vorke (2)
 port id                8002                    state                  blocking
 designated root        8000.16500a8e632a       path cost                100
 designated bridge      8000.42031e2df8ce       message age timer         19.88
 designated port        8002                    forward delay timer        0.00
 designated cost         100                    hold timer                 0.00
 flags


EPSILON:~$ ping vorke.vpn.insom.me.uk
PING vorke.vpn.insom.me.uk (10.99.99.3) 56(84) bytes of data.
64 bytes from 10.99.99.3: icmp_seq=1 ttl=64 time=196 ms
64 bytes from 10.99.99.3: icmp_seq=2 ttl=64 time=196 ms
64 bytes from 10.99.99.3: icmp_seq=3 ttl=64 time=197 ms
```

You can see from the above the Epsilon (US) isn't using its connection to
either Rho (FR) or Vorke (CA). It's only using Bob (UK). And that means when I
use ping, even though Canada and the US share a land mass, my packets take
nearly 200ms to return: *the traffic is going over to England and back,
crossing the Atlantic twice*.

The full script for this is [available in this gist][gist].

[bigtrak]: https://twitter.com/insom/status/843579691604828160
[ug]: https://twitter.com/insom/status/835978638063468546
[kinda]: https://twitter.com/insom/status/816405430079541251
[wg]: https://wireguard.io/
[vxlans]: https://en.wikipedia.org/wiki/Virtual_Extensible_LAN
[qs]: https://www.wireguard.io/quickstart/
[stp]: https://en.wikipedia.org/wiki/Spanning_Tree_Protocol
[gist]: https://gist.github.com/insom/f8e259a7bd867cdbebae81c0eaf49776
