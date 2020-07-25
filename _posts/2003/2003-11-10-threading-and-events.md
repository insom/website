---
title: Threading and Events
date: 2003-11-10
---

[Threading vs. event driven asynchronous applications][t]

[t]: http://pyds.muensterland.org/stories/21.html

I'm beginning to think that there is no framework in Python that suits me, so I'm doomed to write my own. Badly.

I had a brief affair with Medusa, with it's Chain-of-Responsability style selection, stackable handlers, and snappy response. Then I tried to do any non-trivial processing. Oops. I could, as Georg has, use thread queues, but that sounds like hackery to me.

I'm currently implementing an application using (wait for it) CGI. It works out of the box, I don't have to lock resources, and while it performs poorly, it's better than you might think.

I've encapsulated things in a 'Context' object that I pass around, and I use one CGI to route things to handlers via C-o-R. When I deploy it, if the load is great enough, I can write a shim to replace CGI with mod_scgi or mod_python or even Medusa if I decide to work around the event driven model.