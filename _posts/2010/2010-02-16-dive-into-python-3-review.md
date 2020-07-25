---
title: Dive into Python 3 Review
layout: post
date: 2010-02-16
url: /2010/02/dive-into-python-3-review/
categories:
  - Uncategorized
---
_Obligatory Disclaimer: Like many reviewers, I received my copy of the book for free._

First things first, this is a tale of two book reviews. There&rsquo;s [Dive into Python 3][1] (online edition) and [Dive into Python 3][2] (second-user wood edition). And, in my humble opinion, there&rsquo;s a really big gulf between these two.

## Paper {#paper}

I _really_ don&rsquo;t like to be overly negative in reviews; I always try and remember that it&rsquo;s someone&rsquo;s work I&rsquo;m talking about, but the production of the paper version of the book really does leave something to be desired.

As a matter of opinion, it feels like the publisher has tried to fit the book on the smallest volume of paper possible- sections which could do with page breaks or larger headings run into eachother, and chapters which impart a lot of information start to feel like an enslaught.

The style of the book is to relay most of the information should explanatory bullet points following an example piece of code. The code is well spaced, but little things niggle, like the sentance closing a paragraph after the bullet points having no spacing. In fact, there is pretty-much no spacing between paragraphs; I really don&rsquo;t think I&rsquo;m being a typography wonk here, I think it&rsquo;s hard to read.

In the online edition Unicode symbols like &#9312; (a circle with the digit &lsquo;1&rsquo; in it) show which bullets map to which part of the code, but in the print edition it&rsquo;s just (1) (paren, number, paren) in the same monospace that&rsquo;s used for the code itself.

There also appears to be a few places where the Unicode heavy nature of the online edition hasn&rsquo;t been reproduced correctly, the most glaring being on page 54. At the bottom of the [boring stuff you need to understand][3] section, there&rsquo;s some text which says:

> Now think about the possibility of multilingual documents, where characters from several languages are next to each other in the same document. (Hint: programs that tried to do this typically used escape codes to switch &ldquo;modes.&rdquo; Poof, you&rsquo;re in Russian koi8-r mode, so 241 means &#1071; _(Ed: reversed R)_; poof, now you&rsquo;re in Mac Greek mode, so 241 means &#974; _(Ed: w with a ligature above it)_.) And of course you&rsquo;ll want to search those documents, too. 

But in the print edition, you get:

> Now think about the possibility of multilingual documents, where characters from several languages are next to each other in the same document. (Hint: programs that tried to do this typically used escape codes to switch &ldquo;modes.&rdquo; Poof, you&rsquo;re in Russian koi8-r mode, so 241 means &#9633; _(Ed: hollow square)_; poof, now you&rsquo;re in Mac Greek mode, so 241 means &#9633; _(Ed: an identical hollow square)_.) And of course you&rsquo;ll want to search those documents, too. 

Which completely reverses the meaning of this _fairly important_ piece of information. Now, this information is re-iterated throughout the book (see later), so you won&rsquo;t be confused for long, but what&rsquo;s really annoying is how they have correctly printed an [interrobang][4] just 3 inches below! It&rsquo;s not just international characters, the odd &emdash; is displayed as a block too (like page 173).

If I haven&rsquo;t made it clear yet; I would definitely not buy the paper edition. I don&rsquo;t like reading off a screen for long stretches, but HTML is the way this book should be read (on a big monitor, with copious whitespace surrounding everything, and a set of Unicode fonts).

## The Content Itself {#the-content-itself}

There&rsquo;s almost nothing to criticise about the _content_ of the book- anything I do point out is really just a case where the author has taken a different tack than most technical books, and you would want to look out for that.

For example, the book is a narrative. It&rsquo;s like &hellip; a story which by reading, you gain Python knowledge. One of the things which highlights this for me is on page 157 of the print edition (the [refactoring][5] section):

> I don&rsquo;t think I&rsquo;ve mentioned this yet anywhere in this book, so let this serve as your final lesson in string formatting. Starting in Python 3.1, you can skip the numbers when using positional indexes in a format specifier. 

If you skipped the refactoring section, more fool you if you get confused by code which doesn&rsquo;t use positional indices. You could say that when writing this that the author might have revisited the chapter on strings and put it in there but &hellip; it&rsquo;s kind of charming, taken in the context of the whole book.

The only other thing to point out, which is not negative but which you may want to bear in mind, is that this is a Mark Pilgrim book. It spends a _lot_ of time talking about Unicode, character encodings, their importance, and how most people handle all of this wrong. It really drills you on the fact that files don&rsquo;t contain text, they contain bytes, and you really _never_ want to mix them up.

The example chapters (which are very good) deal with building an HTTP client which plays nicely, and not just using &ldquo;urllib.urlopen&rdquo;, drawing presumably on the author&rsquo;s experience writing the [Universal Feed Parser][6]. The XML chapter even has a section on [parsing broken XML][7], something most books wouldn&rsquo;t cover (as we&rsquo;re all taught to believe, and it is specified that, XML should always been well-formed).

All those negative vibes out of the way; this is an exciting book. If you are at all interested in Python 3.x (and you should be, as Python 2.x is an evolutionary dead-end, and I&rsquo;m presuming you are interested in the topic of Python _at all_) you should read this book.

Like with my review of [Expert Python Programming][8], some amount of the fun of reading the book is discovering the new features of the language (yay: sets), and new things that I can do. EPP finally got me to understand generators in Python 2.6, and Dive into Python 3 does an equal or better job with Python 3.1.

The style of (introduction, code sample, bullet, bullet, bullet, closing paragraph) which is used liberally throughout really works well; if a picture&rsquo;s worth a thousand words, dissected code examples must be worth at least a few hundred apiece.

There&rsquo;s useful reference material in there too, like a [really comprehensive introduction to regular expressions][9] (which opens with my favourite regular expression quote) and a listing of [all the &lsquo;magic&rsquo; methods in the language][10]. Again, the regular expressions chapter really needs to be read beginning-to-end, but if you&rsquo;re willing to put in the time, you will almost certainly learn something, no matter how long you&rsquo;ve been using regular expressions.

So, as is unusual with book reviews, if the above makes it sound like a book you want to read &mdash; [just go read it][1].

 [1]: http://www.diveintopython3.org/
 [2]: http://www.amazon.co.uk/gp/product/1430224150
 [3]: http://www.diveintopython3.org/strings.html#boring-stuff
 [4]: http://twitter.com/diveintomark/status/3185432348
 [5]: http://www.diveintopython3.org/refactoring.html
 [6]: http://www.feedparser.org/
 [7]: http://www.diveintopython3.org/xml.html#xml-custom-parser
 [8]: http://www.packtpub.com/expert-python-programming/book
 [9]: http://www.diveintopython3.org/regular-expressions.html
 [10]: http://www.diveintopython3.org/special-method-names.html


