---
title: An Algorithm for a Fair Cleaning Rota
layout: post
date: 2014-02-06
---
At [work][1] we have an ASP-powered business management system that includes, among other things, a cleaning rota. Because on a given day a staff member may be absent (client meetings, illness, holiday) it gained the ability to skip a user for a day.

This system has some implementation issues: the circular list has an edge condition when skipping the most recently hired staff member and the code to email people when the rota has been manually moved on &hellip; doesn&rsquo;t. These are besides the point though, because _the algorithm is biased towards people who are out of the office frequently_.

### The (Bad) Science Bit {#the-bad-science-bit}

Times have changed and more of our staff work from home, often on set days of the week. If you work from home on a Wednesday and a Friday then _at best_ you have 3/5 odds of actually doing the clean up when you&rsquo;re in. _Worse than this_ &#8211; if it lands on you on a day that you&rsquo;re out of the office, it may take 20 working days to cycle back around to you, and then it&rsquo;s still 3/5 odds.

<div class="codehilite">
  <pre><span class="o">&gt;&gt;&gt;</span> <span class="p">(</span><span class="mf">1.0</span> <span class="o">/</span> <span class="mi">21</span><span class="p">)</span> <span class="o">*</span> <span class="p">(</span><span class="mf">3.0</span> <span class="o">/</span> <span class="mi">5</span><span class="p">)</span> <span class="o">*</span> <span class="p">(</span><span class="mi">365</span> <span class="o">-</span> <span class="p">(</span><span class="mi">52</span> <span class="o">*</span> <span class="mi">2</span><span class="p">))</span>
<span class="mf">7.457142857142856</span>
<span class="o">&gt;&gt;&gt;</span> <span class="p">(</span><span class="mf">1.0</span> <span class="o">/</span> <span class="mi">21</span><span class="p">)</span> <span class="o">*</span> <span class="p">(</span><span class="mi">365</span> <span class="o">-</span> <span class="p">(</span><span class="mi">52</span> <span class="o">*</span> <span class="mi">2</span><span class="p">))</span>
<span class="mf">12.428571428571427</span>
</pre>
</div>

There&rsquo;s 4.9 days difference between the most fair (you get picked one in 21 times) and the least fair (you get picked one in 35 times). I have not accounted for bank holidays or annual leave in the above, but the number of days doesn&rsquo;t have much impact on fairness.

### A New Hope {#a-new-hope}

I propose the below:

<div class="codehilite">
  <pre><span class="kn">import</span> <span class="nn">random</span>

<span class="n">staff</span> <span class="o">=</span> <span class="p">{</span><span class="s">'User </span><span class="si">%d</span><span class="s">'</span> <span class="o">%</span> <span class="n">k</span> <span class="p">:</span> <span class="mi"></span> <span class="k">for</span> <span class="n">k</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">21</span><span class="p">)}</span>

<span class="k">def</span> <span class="nf">pick</span><span class="p">():</span>
    <span class="n">most_cleanups</span> <span class="o">=</span> <span class="nb">max</span><span class="p">(</span><span class="n">staff</span><span class="o">.</span><span class="n">values</span><span class="p">())</span> <span class="o">&gt;</span> <span class="nb">min</span><span class="p">(</span><span class="n">staff</span><span class="o">.</span><span class="n">values</span><span class="p">())</span> <span class="ow">and</span> \
        <span class="nb">max</span><span class="p">(</span><span class="n">staff</span><span class="o">.</span><span class="n">values</span><span class="p">())</span> <span class="ow">or</span> <span class="mi">1</span> <span class="o">+</span> <span class="nb">max</span><span class="p">(</span><span class="n">staff</span><span class="o">.</span><span class="n">values</span><span class="p">())</span>
    <span class="n">pool</span> <span class="o">=</span> <span class="p">[]</span>
    <span class="k">for</span> <span class="n">k</span><span class="p">,</span> <span class="n">v</span> <span class="ow">in</span> <span class="n">staff</span><span class="o">.</span><span class="n">items</span><span class="p">():</span>
        <span class="n">shares</span> <span class="o">=</span> <span class="n">most_cleanups</span> <span class="o">-</span> <span class="n">v</span>
        <span class="n">pool</span><span class="o">.</span><span class="n">extend</span><span class="p">([</span><span class="n">k</span><span class="p">]</span> <span class="o">*</span> <span class="n">shares</span><span class="p">)</span>
    <span class="n">choice</span> <span class="o">=</span> <span class="n">random</span><span class="o">.</span><span class="n">choice</span><span class="p">(</span><span class="n">pool</span><span class="p">)</span>
    <span class="k">if</span> <span class="n">random</span><span class="o">.</span><span class="n">random</span><span class="p">()</span> <span class="o">&gt;</span> <span class="mf">0.75</span><span class="p">:</span>
        <span class="k">print</span> <span class="s">'Skipped'</span><span class="p">,</span> <span class="n">choice</span>
    <span class="k">else</span><span class="p">:</span>
        <span class="k">print</span> <span class="s">'Picked'</span><span class="p">,</span> <span class="n">choice</span>
        <span class="n">staff</span><span class="p">[</span><span class="n">choice</span><span class="p">]</span> <span class="o">+=</span> <span class="mi">1</span>

<span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">80000</span><span class="p">):</span>
    <span class="n">pick</span><span class="p">()</span>

<span class="n">results</span> <span class="o">=</span> <span class="p">[(</span><span class="n">v</span><span class="p">,</span><span class="n">k</span><span class="p">)</span> <span class="k">for</span> <span class="n">k</span><span class="p">,</span> <span class="n">v</span> <span class="ow">in</span> <span class="n">staff</span><span class="o">.</span><span class="n">items</span><span class="p">()]</span>
<span class="n">results</span><span class="o">.</span><span class="n">sort</span><span class="p">()</span>
<span class="k">print</span> <span class="s">'Total "unfairness" of the system:'</span><span class="p">,</span> <span class="nb">abs</span><span class="p">(</span><span class="n">results</span><span class="p">[</span><span class="mi"></span><span class="p">][</span><span class="mi"></span><span class="p">]</span> <span class="o">-</span> <span class="n">results</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">][</span><span class="mi"></span><span class="p">])</span>
</pre>
</div>

To create a simulation, I set up 21 fake staff members, and initialise them has having never done the cleaning. The process of picking clean-up on a given day is randomised, but everyone who is tied as having done clean-up the most is excluded from being picked.

Everyone else is added to a list with a weighting based on how many days behind &ldquo;the lead&rdquo; they are. If you&rsquo;ve been skipped twice, it&rsquo;s likely you are 2 or 3 days behind your co-workers. You get one share for each day.

A share is picked at random.

For the purposes of the simulation, I&rsquo;m using a random threshold of 0.75 to decide if someone should be skipped. Obviously in reality that would be based on if they are in the office on a given day.

The system is fair in both the short and long term. I&rsquo;ve run it through 80,000 cycles, and (spoiler alert) it&rsquo;s still fair:

<div class="codehilite">
  <pre>...
Picked User 19
Skipped User 1
Picked User 15
Picked User 7
Skipped User 9
Picked User 8
Skipped User 20
Picked User 20
Total "unfairness" of the system: 1
</pre>
</div>

This is measuring fairness as the difference between the staff member who cleans up the least and the one who cleans up the most.

### Is it really fair? {#is-it-really-fair}

Well: no. There&rsquo;s a pretty good argument to say if you&rsquo;re only in the office 3 days a week that you should only have 3/5 of the chance of being picked as a full-time staff member.

The above is only one possible algorithm, fairer than what we have now: hopefully some discussion will shake out an even better one.

 [1]: http://www.iweb.co.uk/


