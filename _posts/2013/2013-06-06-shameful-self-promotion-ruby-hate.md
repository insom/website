---
title: Shameful Self Promotion / Ruby Hate
layout: post
date: 2013-06-06
---
#### Ruby Hate {#ruby-hate}

I very nearly ended up using Octopress for this blog, instead of rolling my own with [Flask][1]+[FlatPages][2]+[Frozen-Flask][3]. It&rsquo;s a great piece of software but everytime I interact with Ruby, or more accurately, Ruby&rsquo;s tools and ecosystem, I end up crying and gnashing my teeth.

[rbenv][4] + [bundler][5] ended up being a little less magical than rvm, but rbenv wasn&rsquo;t quite doing the right thing with my zsh config, so I had to mess with my paths for the right thing to happen.

(Sidebar: I fully appreciate that it&rsquo;s almost definitely my lack of experience with rubygems, bundler, rvm, rbenv and on-my-zsh that are at fault, and not the tools themselves. I&rsquo;ve internalised so much of how pip and virtualenv work that I&rsquo;ve forgotten that those tools also have their quirks that someone less Pythonic might find equally as frustrating PLEASE DON&rsquo;T EMAIL ME ANGRY COMMENTS, thanks).

If anyone is doing this again, on Mac OS X 10.8 with Xcode and [Homebrew][6] installed:

```
brew install rbenv
brew install ruby-build
rehash
rbenv install 1.9.3-p125
rbenv 1.9.3-p125
```

[The Octopress docs][7] recommend building 1.9.3-p0 but ruby-build complains that my version of GCC is wrong, as it&rsquo;s actually LLVM in GCC&rsquo;s clothing. It then recommended installing GCC from [Homebrew-Dupes][8] and a life of heavy drinking, so I took the coward&rsquo;s way out and built 1.9.3-p125 which is actually LLVM compatible.

That trickery with `PATH` is intended to put the 1.9.3 version of gem, rake and ruby first on the path. I think rbenv is supposed to handle this by adding a fake path to your `PATH`, but that didn&rsquo;t happen for me, and this works, so _shrug_.

Now you can switch to the Octopress directory, `gem install bundler`, `bundle install` and `bundle exec rake` to your heart&rsquo;s content.

#### Shameful Self Promotion {#shameful-self-promotion}

I put myself through this gauntlet of hate after working with [Andrew McCombe][9] to get [forced local Exim delivery][10] working. We both thought &ldquo;that would make a good blog post&rdquo;.

Finally, [ICYMI][11], here are some articles of a technical nature I&rsquo;ve written for the [iWeb Hosting Blog][12] and for [iWeb FTP][13]:

  * [Moving Varnish Caching Logic Into PHP&hellip;][14] &#8211; I wouldn&rsquo;t even remotely recommend doing this anymore, and we never did in production, but the technical details are still kind of neat, I think.
  * [Diagnosing Magento Speed Issues With Strace][15] and gdb, too. This needs expanding, as I&rsquo;ve spent the 6 months inbetween getting progressively better at debugging PHP scripts by poking around the runtime.
  * [Apache Space Core Module][16]. An introduction into writing your own Apache module that I decided to completely ignore when Darren, Ed and I wrote a new Apache module for internal use last week. I followed someone else&rsquo;s example instead. No comment.
  * [Using BGP to Serve High-Availability DNS][17]. If you have a BGP hammer, everything looks like a routing problem &hellip; nail &hellip; thing. Regardless of the analogy, this approach has been rock solid, and I&rsquo;m very proud of it. We&rsquo;ve extended its use to active-passive fail-over of HTTP proxy servers, with similar, great, results. If you already have BGP in your life, adding this means not having to learn [Pacemaker][18].
  * [Six Reasons not to Run your own FTP Server][19] &#8211; my first listicle! Okay, it&rsquo;s a bit salesy, but there&rsquo;s no word of a lie in there.

 [1]: http://flask.pocoo.org/
 [2]: http://pythonhosted.org/Flask-FlatPages/
 [3]: http://pythonhosted.org/Frozen-Flask/
 [4]: https://github.com/sstephenson/rbenv
 [5]: http://gembundler.com/
 [6]: https://github.com/mxcl/homebrew
 [7]: http://octopress.org/docs/setup/rbenv/
 [8]: https://github.com/Homebrew/homebrew-dupes
 [9]: http://www.euperia.com/
 [10]: http://blog.iweb-hosting.co.uk/blog/2013/06/06/forcing-exim-local-delivery-on-ubuntu-for-development/
 [11]: http://en.wiktionary.org/wiki/ICYMI
 [12]: http://blog.iweb-hosting.co.uk/
 [13]: http://www.iweb-ftp.co.uk/
 [14]: http://blog.iweb-hosting.co.uk/blog/2012/11/20/moving-varnish-caching-logic-into-php-with-the-curl-vmod/
 [15]: http://blog.iweb-hosting.co.uk/blog/2012/09/11/diagnosing-magento-speed-issues-with-strace/
 [16]: http://blog.iweb-hosting.co.uk/blog/2012/02/08/lunchtime-project-apache-space-core-module/
 [17]: http://blog.iweb-hosting.co.uk/blog/2012/01/27/using-bgp-to-serve-high-availability-dns/
 [18]: http://www.linux-ha.org/wiki/Pacemaker
 [19]: http://blog.iweb-ftp.co.uk/uncategorized/6-reasons-not-to-run-your-own-ftp-server/


