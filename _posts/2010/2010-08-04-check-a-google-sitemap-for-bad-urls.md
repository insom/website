---
title: Check a Google Sitemap for bad URLs
layout: post
date: 2010-08-04
---
Create cagsmfbu.py:

<div class="codehilite">
  <pre><span class="kn">import</span> <span class="nn">sys</span>
<span class="kn">import</span> <span class="nn">httplib2</span>
<span class="kn">import</span> <span class="nn">xml.dom.minidom</span> <span class="kn">as</span> <span class="nn">md</span>

<span class="n">H</span> <span class="o">=</span> <span class="n">httplib2</span><span class="o">.</span><span class="n">Http</span><span class="p">()</span>
<span class="n">X</span> <span class="o">=</span> <span class="n">md</span><span class="o">.</span><span class="n">parse</span><span class="p">(</span><span class="nb">open</span><span class="p">(</span><span class="n">sys</span><span class="o">.</span><span class="n">argv</span><span class="p">[</span><span class="mi">1</span><span class="p">]))</span>
<span class="n">locs</span> <span class="o">=</span> <span class="n">X</span><span class="o">.</span><span class="n">getElementsByTagName</span><span class="p">(</span><span class="s">"loc"</span><span class="p">)</span>
<span class="k">for</span> <span class="n">loc</span> <span class="ow">in</span> <span class="n">locs</span><span class="p">:</span>
    <span class="n">url</span> <span class="o">=</span> <span class="n">loc</span><span class="o">.</span><span class="n">childNodes</span><span class="p">[</span><span class="mi"></span><span class="p">]</span><span class="o">.</span><span class="n">nodeValue</span><span class="o">.</span><span class="n">encode</span><span class="p">(</span><span class="s">'u8'</span><span class="p">)</span>
    <span class="k">try</span><span class="p">:</span>
        <span class="n">res</span><span class="p">,</span> <span class="n">content</span> <span class="o">=</span> <span class="n">H</span><span class="o">.</span><span class="n">request</span><span class="p">(</span><span class="n">url</span><span class="p">)</span>
        <span class="k">print</span> <span class="s">"</span><span class="si">%s</span><span class="se">\t</span><span class="si">%d</span><span class="s">"</span> <span class="o">%</span> <span class="p">(</span><span class="n">url</span><span class="p">,</span> <span class="n">res</span><span class="o">.</span><span class="n">status</span><span class="p">)</span>
    <span class="k">except</span><span class="p">:</span>
        <span class="k">print</span> <span class="s">"</span><span class="si">%s</span><span class="se">\t</span><span class="s">TOOMANY"</span> <span class="o">%</span> <span class="n">url</span>
    <span class="n">sys</span><span class="o">.</span><span class="n">stdout</span><span class="o">.</span><span class="n">flush</span><span class="p">()</span>
</pre>
</div>

And then

<div class="codehilite">
  <pre><span class="c">% python cagsmfbu.py sitemap.xml | tee output.tdf</span>
</pre>
</div>


