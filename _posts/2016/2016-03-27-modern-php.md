---
date: "2016-03-27T23:25:04Z"
title: "Contribution streak: Modern PHP"
type: "journal"
layout: post
---

(If you think things have been quiet on the journal front, [check out the
updates to my Z80 project][u] - I've been doing those instead for a few days)

[u]: /project/z80/

[Last time][lt], I had added a new model to Cachet but created the database
table and populated it by hand. Laravel seems *really* similar to
[Alembic][] and it also lets you create a migration with a command. In this
case:

    $ php artisan make:migration CreateApiKeysTable
    Created Migration: 2016_03_27_195948_CreateApiKeysTable

[Alembic]: https://flask-alembic.readthedocs.org/en/latest/
[lt]: /journal/2016/03/24/

This creates a skeleton class with an `up` and a `down` method which you can
use to migrate and to rollback, respectively. Alembic fills this with a
reasonably accurate guess of what's changed in your models since the last
migration, but Illuminate/Laravel really do leave it up to the developer.

[The documentation][dox] lists a few examples. Those, along with the existing
migrations written by Cachet developers, are enough for me to end up with a
working migration: \[[Commit][c]]

I've changed my mind about an 'active' flag. It's easy enough to delete and
create new keys. I've added a description too, and told Laravel to manage the
timestamps of the model. This is a neat feature that keeps the `created_at`
and `updated_at` fields up-to-date automatically.

I've always found that knowing the creation date (and last used date, but
let's not get ahead of ourselves) of my GitHub API keys is really useful, so
I'm hoping it'll make a nice touch in the UI.

Speaking of the UI, Cachet uses Bootstrap, so I spent a little time trying to
come up with a form layout that I liked, now that there's at least two pieces
of information that will need to be submitted. I tried horizontal and inline
forms, and I reverted a few times. For now, it's getting late so I'll push
what I have and think about it away from the computer for a bit.

This whole PR is taking a bit longer than I thought that it would, but it's
good to learn a bit more about "modern style" PHP development, as I've been
involved in Magento and WordPress for so long.

[c]: https://github.com/insom/Cachet/blob/7947e40edd802ececa59789804571983e9e60258/database/migrations/2016_03_27_195948_CreateApiKeysTable.php
[dox]: https://laravel.com/docs/5.1/migrations
