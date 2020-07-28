---
title: Making GPG Fingerprints Friendlier
date: 2014-05-28
layout: post
---
I received a [keybase.io][1] invite from [@whiskers75][2], and have set [my profile][3] up.

It&rsquo;s really an ingenious idea: taking away the difficulty of establishing that the owner of a given key is who you think it is- if they can prove control of a Twitter or GitHub account, or web hosting for a domain that you recognise, then you can verify these proofs against their key.

For most the interactions I have online (especially anything that would be signed or encrypted) people are _more_ likely to know me as [@insom][4] than to have met me in person.

They show the last 64 bits of your key fingerprint on your profile, which is important, but I can&rsquo;t help but feel that fingerprints are still _super_ unfriendly. I used to have mine on my business card at Crestnorth &#8211; this did not make proofing my business cards any easier, or win me any friends at the printing company.

[PGPfone][5] used to have users read out a series of words to validate that the connection was secure and that they were talking to the person whom they expected to, with no one listening in.

I was always surprised that this didn&rsquo;t catch on more widely. The `/usr/share/dict/words` on my Macbook has 235,886 words &#8211; enough for 17 bits &#8211; but it contains words like &ldquo;phyllophyllin&rdquo; &#8211; not great for use over the phone.

A better fit for my purposes, is [Ogden&rsquo;s Basic English Word List][6] &#8211; a list of 850 words which are considered &ldquo;basic English&rdquo; &#8211; and useful for learners. This excludes most technical and specific words and ensures widely pronounceable words are chosen. I copied and pasted my [word list from here][7].

[ After writing this post, I&rsquo;ve become aware of a standard word list used for this &#8211; [the PGP word list][8] &#8211; oh, well, it was just a quick hack, anyway. ]

The largest power of two under 850 is 2^9, so we&rsquo;re going to break the fingerprint into 9 bit chunks and then use that 9 bit integer as an index into the alphabetised word list:

<div class="codehilite">
  <pre><span class="c">#!/usr/bin/python</span>
<span class="kn">import</span> <span class="nn">sys</span>
<span class="n">words</span> <span class="o">=</span> <span class="p">[</span><span class="n">x</span><span class="o">.</span><span class="n">strip</span><span class="p">()</span> <span class="k">for</span> <span class="n">x</span> <span class="ow">in</span> <span class="nb">open</span><span class="p">(</span><span class="s">'words'</span><span class="p">)</span><span class="o">.</span><span class="n">readlines</span><span class="p">()]</span>
<span class="n">fp</span> <span class="o">=</span> <span class="n">sys</span><span class="o">.</span><span class="n">argv</span><span class="p">[</span><span class="mi">1</span><span class="p">]</span>
<span class="n">fp_as_long</span> <span class="o">=</span> <span class="nb">long</span><span class="p">(</span><span class="n">fp</span><span class="p">,</span> <span class="mi">16</span><span class="p">)</span>
<span class="n">nine_bits</span> <span class="o">=</span> <span class="p">(</span><span class="mi">2</span> <span class="o">**</span> <span class="mi">9</span><span class="p">)</span> <span class="o">-</span> <span class="mi">1</span>
<span class="c"># 64 / 9 is 7.1 - round up to 8 to use all of our bits.</span>
<span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">8</span><span class="p">):</span>
    <span class="n">word_index</span> <span class="o">=</span> <span class="n">fp_as_long</span> <span class="o">&</span> <span class="n">nine_bits</span>
    <span class="n">fp_as_long</span> <span class="o">=</span> <span class="n">fp_as_long</span> <span class="o">&gt;&gt;</span> <span class="mi">9</span>
    <span class="k">print</span> <span class="n">words</span><span class="p">[</span><span class="n">word_index</span><span class="p">],</span>
<span class="k">print</span>
</pre>
</div>

And we&rsquo;re done! Giving it my fingerprint of `8CCE 2412 3B8F 78F8` I can generate the phone-call-friendly fingerprint of:

> fact minute effect bitter berry card base able

Mmm. Bitter berries.

 [1]: https://keybase.io/
 [2]: https://twitter.com/whiskers75
 [3]: https://keybase.io/insom
 [4]: https://twitter.com/insom
 [5]: http://en.wikipedia.org/wiki/PGPfone
 [6]: http://www.basic-english.org/
 [7]: http://www.manythings.org/vocabulary/lists/l/words.php?f=ogden
 [8]: http://en.wikipedia.org/wiki/PGP_word_list


