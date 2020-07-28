---
title: Dell Inspiron Fan Speed Collectd Recipe
date: 2011-04-04
layout: post
---
First, `modprobe i8k`, then add the following to your collectd config:

<div class="codehilite">
  <pre>    <span class="nt">&lt;Plugin</span> <span class="err">table</span><span class="nt">&gt;</span>
      <span class="nt">&lt;Table</span> <span class="err">"/proc/i8k"</span><span class="nt">&gt;</span>
        Instance i8k
        Separator " "
        <span class="nt">&lt;Result&gt;</span>
          Type gauge
          InstancePrefix "fanspeed"
          InstancesFrom 2
          ValuesFrom 7
        <span class="nt">&lt;/Result&gt;</span>
      <span class="nt">&lt;/Table&gt;</span>
    <span class="nt">&lt;/Plugin&gt;</span>
</pre>
</div>


![][1] ![][2]

 [1]: https://24.media.tumblr.com/tumblr_lj4p8morfT1qaiup8.png
 [2]: https://24.media.tumblr.com/tumblr_lj4p97ysBu1qaiup8.png


