---
title: Graphing Raspberry Pi internal temperature with collectd
date: 2013-07-02
layout: post
---
I&rsquo;m a big fan of [collectd][1], the pluggable metrics collection daemon, and I came across [this post][2] about checking the temperature, so I decided to get collectd up and running on my Pi and pull some graphs out to see if there are any trends.

Previous related posts:

  * [Feeding Current Cost Power Consumption into Collectd][3]
  * [Dell Inspiron Fan Speed Collectd Recipe][4]

#### Installation {#installation}

Because collectd defaults to a 10 second quantum, it will either keep my USB disk drive awake the whole time or wear out my SD card. One option would be to use the &lsquo;[network][5]&lsquo; plugin for collectd and ship the readings off to a bigger machine, but in the interests of being self contained, I&rsquo;ll use a tmpfs filesystem (which is basically a RAM disk).

<div class="codehilite">
  <pre>sudo apt-get install collectd-core
sudo mount -t tmpfs tmpfs /var/lib/collectd/
</pre>
</div>

It won&rsquo;t start because it&rsquo;s missing a configuration, so lets put a basic one together, in `/etc/collectd/collectd.conf`:

<div class="codehilite">
  <pre><span class="nb">LoadPlugin</span> <span class="s2">"logfile"</span>
<span class="nb">LoadPlugin</span> <span class="s2">"rrdtool"</span>

<span class="nb">LoadPlugin</span> <span class="s2">"interface"</span>
<span class="nt">&lt;Plugin</span> <span class="s">"interface"</span><span class="nt">&gt;</span>
  <span class="nb">Interface</span> <span class="s2">"/(veth.*|lo|br)/"</span>
  <span class="nb">IgnoreSelected</span> true
<span class="nt">&lt;/Plugin&gt;</span>

<span class="c">#LoadPlugin "thermal"</span>
<span class="c">#&lt;Plugin "thermal"&gt;</span>
<span class="c">#  Device "thermal_zone0"</span>
<span class="c">#  IgnoreSelected false</span>
<span class="c">#&lt;/Plugin&gt;</span>

<span class="nb">LoadPlugin</span> <span class="s2">"table"</span>
<span class="nt">&lt;Plugin</span> <span class="s">table</span><span class="nt">&gt;</span>
  <span class="nt">&lt;Table</span> <span class="s">"/sys/class/thermal/thermal_zone0/temp"</span><span class="nt">&gt;</span>
    <span class="nb">Instance</span> thermal
    <span class="nb">Separator</span> <span class="s2">" "</span>
    <span class="nt">&lt;Result&gt;</span>
      <span class="nb">Type</span> gauge
      <span class="nb">InstancePrefix</span> <span class="s2">"pi"</span>
      <span class="nb">ValuesFrom</span> <span class="m"></span>
    <span class="nt">&lt;/Result&gt;</span>
  <span class="nt">&lt;/Table&gt;</span>
<span class="nt">&lt;/Plugin&gt;</span>
</pre>
</div>

You can see a commented out section referencing the `thermal` plugin- unfortunately this was broken in the version of collectd that is currently in Raspian Wheezy. The fix is in [this commit][6], but I didn&rsquo;t really want to build collect from source, for instead I&rsquo;m using the [table][7] plugin, and cheating by omitting the `PrefixFrom` parameter.

Start collectd with `sudo /etc/init.d/collectd start` and within a few seconds you should see files start to appear in `/var/lib/collectd/<your hostname>/table-thermal/`. If you don&rsquo;t have a collectd graphing utility, you can generate one using rrdtool. (I use [my own dashboard that I wrote at work][8] usually, but it&rsquo;s not been updated for collectd 5.1, as Ubuntu still ships 4.10 in their LTS releases).

An example rrdtool incantation, and the graph to go with it:

<div class="codehilite">
  <pre>rrdtool graph ~/temperature.png -s -4hour -w 500 -h 100 <span class="se">\</span>
--lower-limit 0 --alt-autoscale-max --slope-mode <span class="se">\</span>
<span class="s1">'DEF:o=/var/lib/collectd/pi/table-thermal/gauge-pi.rrd:value:MAX'</span> <span class="se">\</span>
<span class="s1">'CDEF:oo=o,1000,/'</span> <span class="s1">'AREA:oo#ffcc00'</span>
</pre>
</div>

![A temperature graph from my Raspberry Pi][9]

 [1]: http://collectd.org/
 [2]: http://magnatecha.com/checking-the-cpu-temperature-of-a-raspberry-pi/
 [3]: https://www.insom.me.uk/post/11837001497/current-cost-collectd
 [4]: https://www.insom.me.uk/post/4338064789/dell-inspiron-fan-speed-collectd-recipe
 [5]: https://collectd.org/wiki/index.php/Plugin:Network
 [6]: https://github.com/collectd/collectd/commit/d2c70797b18c2b532119b1264841f551e013dcad
 [7]: https://collectd.org/wiki/index.php/Plugin:Table
 [8]: https://github.com/iwebhosting/collectd-flask/
 [9]: https://f.insom.me.uk/blog-images/whileTrue.png


