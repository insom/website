---
title: Feed Current Cost into collectd
date: 2011-10-23
layout: post
---
I own a Current Cost Envi (CC128), and was recently sent the RJ45<>USB lead by e.on, my power supplier.

Given that the only heating my outside office has is a 1-2kW oil filled heater and that we might have a cold winter, I wanted to estimate how much it costs, and keep and eye on the duty cycle of the heater vs. the outside temperature.

The reading for temperature is that of the receiver (not the unit clamped to your incoming mains supply) &#8211; in my case this is great because the receiver is in the coal-house-data-centre (CHDC) and therefore nearly-outside.

Here&rsquo;s an example graph, after going through [collectd-web][1] and [collectd-flask][2]:

![][3]

[The Python daemon which writes to a file in /tmp is here][4]. And this is the snippet of config you will need to make it all work:

<div class="codehilite">
  <pre><span class="nt">&lt;Plugin</span> <span class="err">table</span><span class="nt">&gt;</span>
  <span class="nt">&lt;Table</span> <span class="err">"/tmp/cctable"</span><span class="nt">&gt;</span>
    Instance currentcost
    Separator "\\t"
    <span class="nt">&lt;Result&gt;</span>
      Type gauge
      InstancePrefix "temp"
      InstancesFrom 0
      ValuesFrom 1
    <span class="nt">&lt;/Result&gt;</span>
    <span class="nt">&lt;Result&gt;</span>
      Type gauge
      InstancePrefix "watts"
      InstancesFrom 0
      ValuesFrom 2
    <span class="nt">&lt;/Result&gt;</span>
  <span class="nt">&lt;/Table&gt;</span>
<span class="nt">&lt;/Plugin&gt;</span>
</pre>
</div>

 [1]: https://github.com/httpdss/collectd-web
 [2]: https://github.com/iwebhosting/collectd-flask
 [3]: https://24.media.tumblr.com/tumblr_ltjh4o8l2H1qaiup8.jpg
 [4]: https://gist.github.com/1307924


