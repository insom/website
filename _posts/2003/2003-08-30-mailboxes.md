---
title: Handling Mailboxes in Python
date: 2003-08-30
layout: post
author: Aaron Brady
categories: foo
---

I've added two new snippets to the hacks section; [save.py & strip.py](/hacks/mailtools.html) - used to save attachments from a whole mailbox, or strip them, respectively.

Python comes with really nice mailbox classes, including QMail maildirs, which is what we use on our servers - but unfortunately these are read only - so strip.py cops out and write mbox files to stdout.

You could always use an mbox2maildir tool when you're finished I guess. Alternatively, you could parse the maildir yourself, and edit the files in place. But I don't need to - so I didn't.
