---
title: Temperature logging, again
layout: post
---

[The last time that I did this][last], in 2016, I had a Grafana stack ready to go.

I've moved twice since then, I've made my peace with Canadian weather (-18C doesn't scare me now!) but I have a separate garage and I don't run any kind of metrics collection stack, nor do I really want to.

([In 2013, I had a collectd stack](/2013/07/02/graphing-raspberry-pi-internal-temperature-with-collectd.html), so I clearly follow fashions)

I have a stash of Dallas DS12B80's that I ordered by mistake back in England. These are OneWire devices, and the Raspberry Pi handles this natively.

I didn't even need strip-board for this, I soldered the part and a 4.7K pull-up straight to some 2.54mm pins:

![Temperature Sensor Close Up](/Gfx/temp/close.png)

I wrote a blank Raspberry Pi OS image to the SD card, and made the following changes on the first partition:

```
mount /dev/sdb1 /mnt
cd /mnt
touch ssh
cat > wpa_supplicant.conf << EOF
update_config=1
country=CA
network={
 ssid="MySSID"
 psk="MyPassword"
}
EOF
echo dtoverlay=w1-gpio >> config.txt
```

To make it as simple as possible to get this data, I have almost the smallest possible Flask app:

```python
from flask import Flask
app = Flask(__name__)
@app.route('/')
def index():
    with open('/sys/bus/w1/devices/28-000007a79b6a/temperature', 'rb') as f:
        return f.read()
```

```
$ curl 192.168.2.55:5000
6062
```

That's 6C. I laser cut a case for the Pi and mounted it on the wall:

![The sensor installed](/Gfx/temp/far.png)

That just leaves collection. It's funny that I have become so used to having Grafana or Datadog for metrics that I forgot that `rrdtool` still exists. It was good enough for MRTG and it's still good enough for me.

(RRD really blazed a trail for fixed size time series data when it was introduced in 1999, as I recall)

We have to create our RRD file in advance and this was always the most arcane part of things. I spent some quality time in the man page for `rrdcreate` before settling on:

```bash
rrdtool create heat.rrd \
  --step 5m \
  DS:c:GAUGE:5m:-50000:50000 \
  RRA:AVERAGE:0.5:5m:10d \
  RRA:AVERAGE:0.5:30m:90d \
  RRA:AVERAGE:0.5:2h:18M 
```

Then we just create a cron job to pull in the results:

```
rrdtool update heat.rrd N:$(curl -s http://192.168.2.55:5000)
```

And we can generate a graph any time we want:

```
rrdtool graph -s '-2d' heat.png DEF:c=heat.rrd:c:AVERAGE AREA:c#FFdddd:"mC"
```

![Aaron's Garage for the last two days](/Gfx/temp/temp.png)

[last]: /2016/12/19/micropython-temperature-logger.html
