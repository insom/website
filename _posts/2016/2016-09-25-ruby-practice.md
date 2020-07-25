---
date: "2016-09-25T16:00:00Z"
title: "Ruby Practice"
type: "journal"
layout: post
---

I got a new job in a new place, and with that job comes a new set of
programming languages.

I've been lucky to be able to mostly code in Python for the last few years.
It's my default language and the closest to the way that I think, but this has
meant I've let other language skills that I have atrophy a bit. The most
relevant of these is Ruby.

I [posted before about exercism.io][eio], it's a great way to get up and
running with a new language, especially if you're already a programmer or have
a little experience. Generally speaking the solutions to the problems you're
given take you on a bit of a trip around the core concepts of each language and
its standard library.

That being said, I was still reaching for Python and not for Ruby when solving
problems. So I've decided that those those little "helper" things I would have done in
Python will now be done in Ruby. I had to do a similar thing when I learned C
(after BASIC); I kept sliding back to BASIC for tasks until I forced myself.

I've got a new broadband supplier and a new router set up. I was previously
terminating my PPPoE on a Raspberry Pi, but now I'm just using the supplier's
router. Also my IP is *way* more unstable on this supplier, so I keep not being
able to SSH in to my house - updating my `home.insom.me.uk` record by hand
isn't going to cut it.

Previously I had this script:

```bash
#!/bin/bash
IP=$(ip a | grep 'inet.*ppp0' | awk '{print $2}')
nsupdate -k /root/ddns.txt <<EOF
server 163.172.162.171
update delete home.insm.cf 300 a
send
update add home.insm.cf 300 a $IP
send
EOF
```

It relied on a BIND TSIG key being in `/root/ddns.txt`. Not having the IP
terminate on the router means I'm going to have to use a third party service to
find out my IP. I've chosen [jsonip.com][jip].

[jip]: http://jsonip.com
[eio]: /journal/2016/04/22/

The [first draft][fd] of the code is pretty basic. It has hardcoded everything
and doesn't handle any errors, but it worked. A few commits later and the
[final version][fv] is over twice as long, mainly due to argument parsing and
trying to be clever about our inputs.

It also gets an ([almost][]) clean bill of health from Rubocop. It sports a
`Gemfile` (for bundler) and a `gemspec`, so I can [publish it on
rubygems.org][pub].

To use it, you'll need a BIND master server for your zone with a TSIG key
configured. There's examples in the [README][]

[README]: https://github.com/insom/dns-update/blob/master/README.md

I suspect not that many people run their own BIND for a small
installation, but I much prefer using an RFC-ed protocol over just some
proprietary or jerry-rigged REST API.

[fd]: https://github.com/insom/dns-update/blob/c6e6a180a89fd031a5e6d980173b1cdfef412883/dns-update.rb
[fv]: https://github.com/insom/dns-update/blob/master/bin/dns-update
[almost]: https://github.com/insom/dns-update/blob/master/.rubocop.yml
[pub]: https://rubygems.org/gems/dns-update
