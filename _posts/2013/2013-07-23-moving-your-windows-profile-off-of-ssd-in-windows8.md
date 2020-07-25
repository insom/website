---
title: Moving your Windows profile off of SSD in Windows8
layout: post
date: 2013-07-23
url: /2013/07/moving-your-windows-profile-off-of-ssd-in-windows8/
categories:
  - Uncategorized
---
**While the below approach worked for me, you should understand each step before attempting it. You should take backups before attempting any system change, especially one which involves moving data and editing your registry**

Yesterday, I [followed this guide from Prasys][1] on how to move your `C:\Users` folder to another drive, because my C: was very small and E: was much larger.

I fully take responsibility for this fact, but it ate my Windows 8 install alive, and I had a fun couple of hours trying to convince Windows to let me even get into safe mode. (You [have to enable it first][2], apparently, probably worth everyone&rsquo;s time to do this)

Reversing the steps (removing the NTFS junction and copying the files back) did not fix my issue.

The most likely thing that went wrong was that the permissions on the `Default` folder got messed up; once I finally got an Explorer window again, I was able to reset these and my machine was a lot happier. I&rsquo;m pretty sure that&rsquo;s what fixed it, anyway.

_So_, now that we&rsquo;ve established that playing with NTFS junctions and `robocopy` is quite dangerous, let me share the solution that actually worked for me. I&rsquo;m going to assume you haven&rsquo;t followed the above steps and half-wrecked your machine, just that you have a user on C: you want to move to E:

#### Create a new administrator user {#create-a-new-administrator-user}

While you&rsquo;re doing this work, create a new administrator account &#8211; you don&rsquo;t want to move an account while it&rsquo;s logged in, so this sacrificial account will be the only one logged in while you do this. Other HOWTO&rsquo;s that I&rsquo;ve seen have you boot to safe mode, re-enable the `Administrator` account, but this will avoid that step.

#### Log everyone else out {#log-everyone-else-out}

You don&rsquo;t want have anything else running on the machine, so log out of your normal accounts and only have the new temporary administrator account you&rsquo;ve created logged in.

#### Create a new `Users` folder {#create-a-new-users-folder}

<div class="codehilite">
  <pre>mkdir E:\Users
</pre>
</div>

#### Copy the data over with `robocopy` {#copy-the-data-over-with-robocopy}

With an administrative command prompt run:

<div class="codehilite">
  <pre>robocopy <span class="n">/mir</span> <span class="n">/copyall</span> C:\Users\Aaron E:\Users\Aaron
</pre>
</div>

This _will delete anything at `E:\Users\Aaron` if it already exists_.

#### Update the profile folder in the Windows registry {#update-the-profile-folder-in-the-windows-registry}

Look in `HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion\ProfileList` for a list of profiles.

![][3]

Just edit `ProfileImagePath` to point to your folder on `E:`, log out of your temporary account, and log back in as your original user.

Open a command prompt and verify that it&rsquo;s opened with your new profile path. If you&rsquo;re happy, you can delete the temporary user that you created, and the copy of your data from the `C:` drive.

<div class="codehilite">
  <pre>rmdir <span class="n">/S/Q</span> C:\Users\Aaron
</pre>
</div>

You&rsquo;re done!

 [1]: http://prasys.info/2012/11/move-the-users-directory-from-ssd-to-hdd-in-windows-8/
 [2]: http://www.thewindowsclub.com/safe-mode-in-windows-8
 [3]: https://f.insom.me.uk/blog-images/win8registry.png


