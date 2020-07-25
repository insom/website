+++
date = "2016-03-22T19:45:04Z"
title = "Contribution streak: Hacking on Cachet"
type = "journal"
+++

Okay, I've chosen today's project to try and contribute to. I went to a talk
at [Staffs Web Meetup][swm] where [James Brooks][jb] presented
[Cachet][chq], a PHP application for running a status page &mdash; those pages
like http://status.github.com/ which show you if a service is
having problems and when they're likely to be fixed.

[jb]: https://james-brooks.uk/
[swm]: http://staffswebmeetup.co.uk/
[chq]: https://cachethq.io/

At the time I remember asking about components and dependencies - I wanted to
be able to mark something like a router or power distribution unit down and
have any affected customers see it on their page, while smaller failures
wouldn't show for customers who weren't affected.

Actually, we have relatively few outages, thankfully, and haven't ever needed
something quite as detailed as Cachet &mdash; so I shelved the idea and didn't
even get around to installing it. I did grab a nice sticker for my laptop,
though.

<!-- Laptop Sticker -->

Well, it's time to earn that sticker. I've found a reasonably sized issue with
no PR attached: [#496][pr]. API tokens are currently one per user, but it
would be better if users could have more than one. I don't know Laravel, but I
think I could do this!

[pr]: https://github.com/CachetHQ/Cachet/issues/496

---

Step #1: Get PHP installed. Cachet currently requires a PHP newer than 5.5.9
(Laravel have dropped support for 5.5 altogether upstream). Ubuntu Wily has a
new enough one, and I grabbed the packaged Composer while I was there.

    apt-get install php5 php5-gd php5-mcrypt composer

Step #2: Follow the [excellent installation instructions][i]. I want some test
data so I've also run `php artisan cachet:seed` to get fixtures.

[i]: https://docs.cachethq.io/docs/installing-cachet

---

Okay, now I'm at the point I'm going to have to read things. The database
access layer seems to be called Illuminate and the [documentation looks
good][d]. It seems like I'll need to create a migration to move the API keys
from the User model onto a new API Key model, but &ndash; I'm going to need to
create that new model first.

[d]: https://laravel.com/docs/5.2/migrations

I don't want to do *too* much reading, so I'll poke around some code.
`Component` and `Incident` models have a parent-child one-to-many relationship. It
looks like this is done by an `incidents()` method on the `Component` and a
`component()` call on the `Incident`.

    124     public function incidents()
    125     {
    126         return $this->hasMany(Incident::class, 'component_id', 'id');
    127     }

    135     public function component()
    136     {
    137         return $this->belongsTo(Component::class, 'component_id', 'id');
    138     }

This `belongsTo`/`hasMany` stuff seems cool. An alternative to using
decorators or introspection to build an ORM.

I've created an `ApiKey` model based off of `User`, and added methods to both
which mirror the two above. \[[Commit][c]]

[c]: https://github.com/insom/Cachet/commit/dd8de115625caa01cad2b53a606f3100eb5a6412

That went okay. I suppose the next thing is to get these keys visible on the
front end. A bit of digging gets me [this .blade.php file][b], which looks a
bit like twig or Jinja, but with extra syntax.

[b]: https://github.com/insom/Cachet/blob/9844d0cff4c59e83b69637d2061e8c8c6741a457/resources/views/dashboard/user/index.blade.php

I've created a for loop to iterate over the apiKeys using that method I just
added, and made up a format for the API call to delete a key. \[[Commit][c2]]

As a bonus, it looks like the wording for revoking a key is already in the
translations file. Perhaps it was called "revoke" before "regenerate", in the
past?

[c2]: https://github.com/insom/Cachet/commit/2493f40abbad63c1267ecd1f0fcbe2d653e0d303

I'm not quite at the point of writing data in using the models or a factory,
so let's cheat and put data directly into the database:

    sqlite> CREATE TABLE api_keys (id INTEGER NOT NULL,
        user_id INTEGER NOT NULL, active TINYINT(1) NOT NULL DEFAULT 1,
        api_key VARCHAR NOT NULL);
    sqlite> INSERT INTO api_keys VALUES (1, 1, 1, "FOOBAR");

A quick refresh of the page (after a `php artisan app:update`) shows our
FOOBAR in all of it's glory. To make the revoke button work I've added a route
and changed the regenerate method to one that deletes the API key.
\[[Commit][c3]]

[c3]: https://github.com/insom/Cachet/commit/a17be7868f4b80675aaed7d5898aee8d74cb2a86

That works too, but now I'm out of time. I'm not going to get this pull
request finished tonight, but at least I have gotten a good grip on the
problem.

Laravel actually seems really nice, and if I ever saw myself writing an
application in PHP again, I would consider using it as a base. Cachet is a
nicely structured app, with good documentation and it seems really easy to get
started with development on it.
