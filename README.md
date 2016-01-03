# lapis - CodeRED 2015

Microsoft Azure + Microsoft Minecraft = On-Demand Minecraft Hosting

A nice little project for self-hosting a Minecraft server on the vastly
superior unmanaged cloud hosting service.

Created by The Doodle Corporation - Randall and Michael.

## Overview

The aim of this project is to allow users to run their own Minecraft
servers on a pay-per-minute basis via Microsoft Azure. This is ideal
for groups of players who enjoy playing on a server together but may
not play for large amounts of time.

lapis is meant to be deployed to a small, always-online server. It acts
as a control panel for users to manage Minecraft servers. A distinction
between users and administrators allows server administrators to control
the finer details of their server, while users have the ability to
boot-up an offline server for playing.

## Installation

You'll need a few things before you try installing lapis.

* `sudo npm install -g azure-cli`
* `sudo pip install Flask`
* `sudo pip install gunicorn`
* `sshpass`

Once you've got those taken care of, go ahead and clone this to your
machine and run `./start.sh`. As long as this is running, you will
be able to access lapis. (You might want to set this up as a service
or just start it in a `screen` session!)

Once the process is running, visit the web domain of your machine
and start the setup process! Follow the steps there and you'll
be good to go!

## Warning / Disclaimer

Remember, this will need access to your Microsoft Azure account in
order to function. If your server becomes compromised, they will have
access to your account, including the ability to spin up an absolutely
ridiculous number of services.

**Do not let this happen. Secure your server!**

We claim no responsbility for any problems that may arise while using
this software. We do our best to put out quality, secure software, but
this is provided as-is with no concept of liability nor warranty. Use
at your own risk!

**Have fun!**
