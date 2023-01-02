---
title: Self Hosting Mastodon
layout: post
---

![Basement Rack Cabinet with three mini-PCs and an external RAID array](https://sbom.tilde.website/media_attachments/files/109/372/182/276/406/005/original/2beeeb503ce50dff.jpg)

I host [tiny.tilde.website][ttw] and some other small things from the basement of my house. I've [written before about][b4] why that's important to me (vs. just using cloud services), but I'd like to share a bit about how it works -- in case it's useful for anyone else or it happens to be useful to future-me when I forget something 😀

I wouldn't call this guide a _best practice_ -- it's just how I've done it. I've built more secure and robust configurations in the past, generally when it's been my job. I take the security of the services I host and their data seriously, but this is still a hobby and I think the uptime and security levels are commensurate.

### Machines

- Nook (a 6th Generation Intel NUC with 256GB SATA SSD and 8GiB RAM)
- Bluebottle (Celeron N3010 with 128GB M2 SATA SSD and 8GiB RAM)
- [Eccles][goons] (Celeron N3010 with 128GB M2 SATA SSD and 8GiB RAM)

None of these machines are a power-house and they were largely picked for cost and low power consumption. `ttw` used to run from a Xeon server which was both power hungry _and still kinda slow_ because it was so old.

[ttw]: https://tiny.tilde.website/
[b4]: https://www.insom.me.uk/2022/05/29/outage.html
[goons]: https://en.wikipedia.org/wiki/Eccles_(character)

Bluebottle and Eccles were bought as a pair, so I could move closer to a high-availbility configuration. I didn't want to go all the way to fully automatic failovers etc. -- this is still a human scale operation, thanks -- but it would be nice for a hardware failure or maintenance to not result in extended downtime or restoring things from backups.

### Linux and Docker

Everything runs Debian 11. I've used Ubuntu on servers since 6.06 Dapper, but the gap between Debian and Ubuntu (for my purposes) has closed and Ubuntu is constantly doing things I don't personally appreciate (like using `netplan` to configure NICs and moving to `snap` over Debian packages for some software). About a year ago I decided to go back to Debian (which I used since 1.3 Bo -- before I was lured away to Ubuntu...). It's sure nice to have `/etc/network/interfaces` back!

I also run everything of importance in Docker. I'm still using Docker CE and haven't investigated moving to Podman. tbh, I don't think this matters to me, unless Docker introduces some onerous licensing conditions I don't want to comply with. There's lots of reasons to like and to not like Docker. Personally I dislike the networking parts, so I run my containers with host networking. This makes them less "contained" but I don't expect security from using Docker, I just want a convenient way to package software.

I use LVM for managing my disks: life is too short to find out your partition needs to be bigger than you first planned and now you're fucked.

### Networking and HTTPS

Even though I have 1Gbit/s fibre to the home (💖), my ISP prohibits hosting public services and I have a dynamic IP. Bending the rules a little, I terminate my incoming connections on a DigitalOcean $5 droplet running WireGuard and nginx. Each physical machine in my basement has its own IP and tunnel back to the droplet.

This is like a self-built version of [Tailscale Funnel](https://tailscale.com/kb/1223/tailscale-funnel/), which is in alpha as I write this, but I'm very excited for them to enable more of this kind of hosting in the future.

[Michael F. Lamb][ml] has a great write-up on how he achieves the same thing.

[ml]: https://orbital.rodeo/~mike/20220808-home-hosting-via-wireguard/

I also use DigitalOcean for my DNS, which is helpful when it comes to Let's Encrypt certificate renewal, as we can use the DNS challenges which are way more convenient than the HTTP ones. [DigitalOcean have their own tutorial for this][dodns].

[dodns]: https://www.digitalocean.com/community/tutorials/how-to-acquire-a-let-s-encrypt-certificate-using-dns-validation-with-certbot-dns-digitalocean-on-ubuntu-20-04

I run something basically the same as the upstream [Mastodon proxy configuration][mpc] and also the [object proxy configuration][opc] for Amazon S3 (where assets are stored). Instead of `localhost:3000` etc. I simply use the WireGuard IPs for the `web` containers (which run Puma).

[mpc]: https://github.com/mastodon/mastodon/blob/main/dist/nginx.conf
[opc]: https://docs.joinmastodon.org/admin/optional/object-storage-proxy/

### Docker (again) and Building Mastodon

For years I kept a local fork of Mastodon with the config for `ttw` and some specific local tweaks in it. This is _fine_ and just meant a `git pull --rebase` and some occasional fixing, but it's a mess once you expand beyond a single server. At that point I'd want a remote to push to, somewhere, but then I need to think about secrets management. Ugh.

Recently I've separated the image building and the Docker Compose configuration. This is a boon because Docker Compose was where I get the most conflicts anyway, and it gives me a tiny surface for the local / secret stuff, instead of having it sit as a few patches on top of a gigantic git checkout.

I have a Makefile and some YAML files in that directory:

```makefile
.PHONY: all clean image
all:
        rsync -Pvrax --delete ./ bluebottle:masto/
        rsync -Pvrax --delete ./ eccles:masto/
clean:
        rm mastodon.docker
mastodon.docker:
        docker image save tootsuite/mastodon -o mastodon.docker
image: mastodon.docker all
        @echo
```

The flow of upgrading for me is now (on Nook):

```
$ cd ~/Repo/mastodon # which only exists on Nook
# ^ a pristine checkout of Masto or glitch-soc
$ docker build
$ cd ~/masto # config directory, just what's needed locally
$ ls
docker-compose-bluebottle.yml
docker-compose-eccles.yml
docker-compose-nook.yml
env.production
Makefile
run
$ make image
$ ./run
```

A more mature solution would be to run my own Docker repository to push the image to, but exporting it is lo-fi and works fine with a limited number of hosts.

On Eccles and Bluebottle the steps are:

```
$ cd ~/masto
$ docker image load -i mastodon.docker
$ ./run
```

Here's a [gist with the YAML files][gist]. It's like the upstream config but:

- `network_mode: host` everywhere.
- `ulimits` added to the web process to stop it eating all of the RAM. Ruby, man. 😅
- `env_file: env.production` everywhere.
- `command: bundle exec sidekiq -c 25 -q push -q pull -q ingress -q default -q mailers` on Eccles and Bluebottle, to ensure that the `scheduler` queue is only run on _one_ server. (Very important).

Elasticsearch and Redis currently only run on one node, and `env.production` needs to be updated if they get failed over.

[gist]: https://gist.github.com/insom/e18fa0d71f9a6ca221fbff3eb6171ffc

### DRBD and PostgreSQL

The whole point of having two matched machines was to get some high availability. The two biggest SPOFs in my whole set up are:

- The DigitalOcean droplet, which requires minimal maintenance and is easy to rebuild.
- The PostgreSQL database, which is vital to the operation and full of irreplaceable data.

Redis, Elasticsearch etc. can be treated as ephemeral: HA would be nice, but if they fail, they can be rebuilt on a blank instance pretty quickly with minimal effort. Rebuilding or even moving PostgreSQL has been the source of most of my stress in running `ttw`.

Because of the burden of getting PostgreSQL hosting right, I've outsourced it since 2021 to Amazon RDS. This has been a little expensive (around C$50/month) and tbh it's unneccessary. I ran PostgreSQL in-house for most of `ttw`'s existance and I'd like to do so again.

To avoid it being a total pain to perform maintenance, I want to be able to easily move PostgreSQL between machines without the ~2 hour downtime window required for a dump and restore of the database. Enter DRBD.

[DRBD is a distributed, replicated block device][drbd]. You can consider it to be like a RAID1 across two servers, where only one server at a time can mount the block device.

My configuration is minimal:

```
# /etc/drbd.d/drbd1.res
resource drbd1 {
 meta-disk internal;
 device /dev/drbd1;
 net {
  verify-alg sha256;
 }
 on eccles {
  disk   /dev/eccles-vg/drbd1;
  address  192.168.2.103:7789;
 }
 on bluebottle {
  disk   /dev/bluebottle-vg/drbd1;
  address  192.168.2.104:7789;
 }
}
```

Then I add the resources on both servers and mark one of them as primary:

```
# On Eccles
lvcreate -L50G -n drbd1 eccles-vg
drbdadm create-md drbd1
drbdadm up drbd1
drbdadm primary drbd1 --force # first time only!
mkfs.ext4 /dev/drbd1
mount /dev/drbd1 /mnt
```

```
# On Bluebottle
lvcreate -L50G -n drbd1 bluebottle-vg
drbdadm create-md drbd1
drbdadm up drbd1
drbdadm secondary drbd1
```


During the initial set up, both sides of the device do not know who the primary should be so, for safety, they both refuse to become primary unless forced. After initial set up, issuing `primary` or `secondary` `drbdadm` commands should be much safer -- DRBD will refuse to make a known-dirty disk primary by default.

There's _yet more Docker_ in here because one thing I like about this configuration is that I can make the configuration move with the data by colocating them on the same block device, so I have `/mnt/pg` for the Docker Compose config and `/mnt/postgres-data` for the actual volumes. Then after a failover, once I have mounted the disks I can just do `cd /mnt/pg && docker-compose up -d` and have a working database 🪄

```yaml
version: '3'
services:
  db:
    restart: always
    image: postgres:14-alpine
    shm_size: 256mb
    network_mode: host
    command: postgres -c max_wal_size=2GB -c max_connections=200 -c shared_buffers=4GB -c min_wal_size=192MB
    healthcheck:
      test: ['CMD', 'pg_isready', '-U', 'postgres']
    volumes:
      - /mnt/postgres-data:/var/lib/postgresql/data
    environment:
      - 'POSTGRES_HOST_AUTH_METHOD=md5'
      - 'POSTGRES_PASSWORD=redacted'
```

[drbd]: https://en.wikipedia.org/wiki/Distributed_Replicated_Block_Device

### Future Work

The PostgreSQL server isn't actually running the production database yet. Gotta take a maintenance window for that one.

Using repointable DNS names or virtual-IPs for the services would make failovers cleaner; right now I need to restart every container if I move a service.

Elasticsearch could run as a cluster, although it's not very heavily used, so maybe that's just wasting RAM.

It'd be nice to make Nook less of a single point of failure.
