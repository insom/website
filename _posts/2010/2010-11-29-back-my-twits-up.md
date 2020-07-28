---
title: Back My Twits Up
date: 2010-11-29
layout: post
---
My first published code in quite a long time, [bmtu][1].

I like reading my old notebooks, I did that [recently][2] with my physical notebooks, but nothing serves as a nearly-real-time diary of my life in the same way that [my Twitter account][3] does.

However, the public Twitter site isn&rsquo;t really a permanent store for that information: it may disappear over night, they may have an horrific crash or, for perfectly reasonable performance reasons, they may expire or remove access to old tweets. In fact, you can only go about 3,200 posts back, so if you&rsquo;re prolific, it may make sense to start backing up now.

[Trevor][4] pointed me at [Tweet Nest][5], but it does a lot of things I don&rsquo;t need (like analytics) and it uses an environment that I don&rsquo;t run on my hosting (PHP, MySQL). The homepage is vocal about being tested in LAMP environments. I run Linux/Nginx/SQLite/Python &#8211; a LiNgSqPy stack. Catchy.

If you have PHP and MySQL hosting, or you don&rsquo;t know what you have, you should probably stop here and just install [Tweet Nest][5]. If you have some ill-defined and lofty idea of software minimalism, but not so minimal that it doesn&rsquo;t pull in a (smaller) SQL database engine, please check out [the project&rsquo;s Github page][1].

bmtu is designed to recover when it fails, and run periodically from a cron, where it will slavishly update an SQLite database in your home directory with the latest 140-character wisdom from any user (who doesn&rsquo;t have a private timeline!) you give as a parameter. It uses 2+ anonymous API calls per hour, and comes with a README explaining its use. It&rsquo;s licensed under an MIT-X11-style license.

 [1]: https://github.com/insom/bmtu
 [2]: http://instagr.am/p/YZVv/
 [3]: https://twitter.com/insom
 [4]: http://www.trovster.com/
 [5]: http://pongsocket.com/tweetnest/


