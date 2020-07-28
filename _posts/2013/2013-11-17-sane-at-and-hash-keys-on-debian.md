---
title: Sane At and Hash keys on Debian
layout: post
date: 2013-11-17
---
I say sane, and I&rsquo;m not being totally fair:

I learned to type on a US keyboard. This is mostly because that was the default in DOS if you didn&rsquo;t bother to change it and, being Irish, I didn&rsquo;t see any reason why I would pick `English (British)` as a key layout.

Early computers that I had access to (8088 represent) were US imports previously used for industrial control applications at my dad&rsquo;s work, so the keycaps matched what happened on the screen, too.

As I learned to program, especially in C, the fact that US keyboards&rsquo; default to putting # under `Shift-3` was far more useful than &pound; was. (We still used &pound; in Ireland at that point, but I personally used # a lot more).

Since moving the UK, I&rsquo;ve endeavoured to learn to type like a Brit. It was going well until a couple of years ago, when I got a MacBook Pro [from work][1]. Even with the British keyboard option, Apple makes `Shift-2` into @. In a worst of both worlds situation though, it _also_ sets `Shift-3` to be a &pound;.

I fixed the latter with a Mac keyboard layout called [Programmers British][2], pretty much turning a MacBook Pro British keyboard into the US keyboards of my youth. I don&rsquo;t think I could work without this keyboard layout.

_Now_, when I go back to using my personal Dell laptop I find myself pressing all of the wrong keys. I&rsquo;ve resisted changing this because I like to train myself to use computers as I find them: as a System Administrator I use lots of computers and keyboards that are not set up just like I want, and you need to roll with it. This is fine for occasional use, but when you&rsquo;re trying to get _real work done_ it&rsquo;s infuriating.

I found an [Ubuntu guide for custom keyboard layouts][3] and a bit more Googling around and digging into XKB got me what I needed. The process is not painless, even when you do what appears to be the &lsquo;right thing&rsquo;. You need to add a file in `/usr/share` (which isn&rsquo;t great) and you need to edit a file which is provided by the distribution (which _really_ isn&rsquo;t great).

This is `/usr/share/X11/xkb/symbols/insom`:

<div class="codehilite">
  <pre>partial default alphanumeric_keys
xkb_symbols "basic" {
    include "gb(basic)"
    name[Group1]="English (UK, Sane @/#)";
    key &lt;AE02&gt;  { [2, at, twosuperior, oneeighth ] };
    key &lt;AE03&gt;  { [3, numbersign, threesuperior, sterling ] };
    key &lt;AC11&gt;  { [apostrophe, quotedbl, dead_circumflex, dead_caron] };
    include "level3(ralt_switch_multikey)"
};
</pre>
</div>

It&rsquo;s actually pretty straightforward what&rsquo;s going on here, identifiers like `<AE02>` map on to physical keys and the `{ }` contains a 4-tuple of the key, key with shift, key with alt green, and key with shift and alternate green.

It&rsquo;s nice that we&rsquo;re keeping the copy & paste down by including the basic UK layout `gb(basic)`, so it&rsquo;s just keys we&rsquo;re overriding here. As well as changing the behaviour of `Shift-2` and `Shift-3`, I&rsquo;m changing `Shift-'` &mdash; otherwise there wouldn&rsquo;t be a way to output a double quote.

Sadly, we need to edit `/usr/share/X11/xkb/rules/evdev.xml` and add a stanza of XML. This is so that the `Region and Language / Layouts` pane in GNOME knows that we&rsquo;ve added a new language.

You may be able to select this language without logging out and in, but for me it appeared in the languages bar with no text (though it did work). Logging back in or even rebooting should cause all the right things to fall into place.

<div class="codehilite">
  <pre><span class="nt">&lt;layout&gt;</span>
  <span class="nt">&lt;configItem&gt;</span>
    <span class="nt">&lt;name&gt;</span>insom<span class="nt">&lt;/name&gt;</span>

    <span class="nt">&lt;shortDescription&gt;</span>en<span class="nt">&lt;/shortDescription&gt;</span>
    <span class="nt">&lt;description&gt;</span>English (UK, Sane @/#)<span class="nt">&lt;/description&gt;</span>
    <span class="nt">&lt;languageList&gt;</span>
      <span class="nt">&lt;iso639Id&gt;</span>eng<span class="nt">&lt;/iso639Id&gt;</span>
    <span class="nt">&lt;/languageList&gt;</span>
  <span class="nt">&lt;/configItem&gt;</span>
<span class="nt">&lt;/layout&gt;</span>
</pre>
</div>

 [1]: http://www.iwebsolutions.co.uk/
 [2]: https://twitter.com/insom/status/222451533638410240
 [3]: https://help.ubuntu.com/community/Howto%3A%20Custom%20keyboard%20layout%20definitions


