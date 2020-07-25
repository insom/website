+++
date = "2016-06-22T22:02:12Z"
title = "Generating a Let's Encrypt certificate from a different machine"
type = "journal"
+++

This one is basically a HOWTO I've been meaning to write up. I may need a whole
new template in Hugo for this kind of thing, if I make a habit of it.

There are situations where you may want to use a [Let's Encrypt
certificate][le] but you can't run the client on the target machine. Two that
I've come across are:

* Hosting without shell access
* *Very* small VMs without enough RAM to run the full [Certbot client][cb]

Also, because you shouldn't run anything as root that you don't need to, let's
make the whole thing work for our regular user account. You're going to need
Python's virtualenv package (`sudo apt-get install python-virtualenv` on Debian
or Ubuntu), as well as `git` for the next step. All of the smarts can run on
any machine you trust, such as a laptop, local VM or even on a MacBook.

Clone [Certbot][cb] and [pick a release][p] to check out:

    git clone https://github.com/certbot/certbot
    cd certbot
    git checkout v0.8.1

Okay, now we'll make a virtualenv - this is a private Python installation that
we can install packages into without root permissions, and allows us to avoid
conflicts that might arise from installing conflicting versions of packages for
different applications.

    virtualenv venv

And we'll install our checked out copy of Certbot into our virtualenv:

    venv/bin/python setup.py install

Lots of text will scroll by, hopefully it worked for you. Let me know if not.

Now we have Certbot installed locally, we'll need to set up some directories
for it to work with. It defaults to using system directories which require
running as root, but we really don't want to do that. Let's make our own:

    mkdir -p ~/.le/etc ~/.le/var/lib ~/.le/var/log

And let's register our certificate:

    venv/bin/certbot certonly --text -d arko.insm.cf --keep-until-expiring \
    --agree-tos --config-dir ~/.le/etc --work-dir ~/.le/var/lib --logs-dir \
    ~/.le/var/log --manual --register-unsafely-without-email

You need to swap out `arko.insm.cf` for your own domain name - the one which
currently points at your remote hosting. You can specify more than one `-d`
option with more than one domain, but they will all need to be reachable for
verification. I just need one.

You'll get a wall of text, including a warning that your IP will be logged,
which I've agreed to and you will need to, too.

    -------------------------------------------------------------------------------
    NOTE: The IP of this machine will be publicly logged as having requested this
    certificate. If you're running certbot in manual mode on a machine that is not
    your server, please ensure you're okay with that.

    Are you OK with your IP being logged?
    -------------------------------------------------------------------------------
    (Y)es/(N)o: y
    Make sure your web server displays the following content at
    http://arko.insm.cf/.well-known/acme-challenge/2qruN2PEJL_-7OBFUSCATEDxhrHLazCOr3UFNrCBJbQ before continuing:

    2qruN2PEJL_-75R2436OBFUSCATEDzCOr3UFNrCBJbQ.mGoimgyJQKeruGrLgfDglJlhFMDvhcWLYIV2FNBOWhM

Okay, so just create a file called
"`2qruN2PEJL_-7OBFUSCATEDxhrHLazCOr3UFNrCBJbQ`" with the contents
"`2qruN2PEJL_-75R2436OBFUSCATEDzCOr3UFNrCBJbQ.mGoimgyJQKeruGrLgfDglJlhFMDvhcWLYIV2FNBOWhM`,".
Your value for both the filename and the contents *will be different* so you
can't just copy them from this post.

Upload your file to the `.well-known/acme-challenge` folder on your web hosting.
Once you've done that, press enter on the client to let the Let's Encrypt
servers continue with their challenge.

If it's successful, you'll get a message like this:

	IMPORTANT NOTES:
	 - Congratulations! Your certificate and chain have been saved at
	   /home/aaron/.le/etc/live/arko.insm.cf/fullchain.pem. Your cert will
	   expire on 2016-09-20. To obtain a new or tweaked version of this
	   certificate in the future, simply run certbot again. To
	   non-interactively renew *all* of your certificates, run "certbot
	   renew"
	 - Your account credentials have been saved in your Certbot
	   configuration directory at /home/aaron/.le/etc. You should make a
	   secure backup of this folder now. This configuration directory will
	   also contain certificates and private keys obtained by Certbot so
	   making regular backups of this folder is ideal.
	 - If you like Certbot, please consider supporting our work by:

	   Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
	   Donating to EFF:                    https://eff.org/donate-le

The private key will be in your `~/.le/etc/live/<domain>/` directory, along
with the certificate, CA chain, and CA chain with certificate in one bundle
(fullchain.pem).

You should refer to your webserver or web hosting's instructions on how to
install the certificates, but that's the process of obtaining them done.

The way that I've run the command will not result in you getting notified about
your certificate expiring, so you should place a reminder for yourself around
80 days in the future to repeat this process.

[cb]: https://github.com/certbot/certbot
[p]: https://github.com/certbot/certbot/releases
[le]: https://letsencrypt.org/
