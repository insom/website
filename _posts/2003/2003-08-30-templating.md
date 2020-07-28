---
title: Templating
date: 2003-08-30
layout: post
---

I have spent three (3) days writing templating code.

I initially found [Cheetah][] and feel in love. It made lots of sense, and it took advantage of inheritance etc.

[Cheetah]: https://cheetahtemplate.org/

But, given a sufficiently clean piece of code (like Cheetah), I'm disinclined to write ugly hacks around it. So I went in search of the best way of using inheritance to do what I want, and I duly found that in my particular case I could make data flow from the super-class to sub-classes, or with sub-classes up to the super-class, but to do both I had to tightly couple them.

Worse, when trying to create my own classes as super-class (or as sub-class, I tried a lot of things) I ended up tying the templates to my code, and my code directly to the templates. Moving things broke things.

Worse still, inheritance is fine way of doing things, until you start using dynamic templates (that is; sourcing them from files, or RDBMS) instead of static ones (that is; compiled into a .py from a .tmpl).

So, I set about writing my own little template language, based on keeping it simple. How simple can you get and still be useful? Well, SSI. Hence, PySSI was born, and it had a syntax something like this:

    <!--#py-include virtual="file:tmpl/Header.tmpl"-->
    <!--#py-eval expr="zen = 1"-->
    <!--#py-echo expr="zen+1"-->
    <!--#py-include virtual="file:tmpl/Footer.tmpl"-->

All was good (in less than 40 lines of Python), until I decided that I didn't want HTML littering my Python, so how could I do one row of an HTML table for each line of a file? Well, I'd need a 'for' command.

PySSI2 abandoned the traditional SSI command look, instead looking like this:

    <!--[if expr="1==2"]-->Don't print this ...<!--[/if]-->
    <!--[if expr="1==1"]-->But, *do* print this - $$words $words<!--[/if]-->
    <!--[for expr="[1,3,4]" var="x"]-->
    <!--[for expr="[1,3,4]" var="y"]-->
    Do $y.
    <!--[/for]-->
    <!--[/for]-->

Well, there were problems here too. For one thing, it didn't work. I implemented things by using re.split(), breaking everything into tokens, flex(1) style, but then to implement for loops I had to 'peek' ahead and repeat things (or delete them for 'if's). This was a rank idea, so I made a third stab.

PySSI3 made a parse-tree out tokens, worked fine, and had a syntax like this:

    #for x in range(4):
    #for y in range(x):
    #if x > 2:
    $y
    #end if
    #end for
    #end for

Yes, three days of work, and I had slowly rewritten a crappy version of Cheetah. Joy. Back to using Cheetah (and having to do ugly things with it).
