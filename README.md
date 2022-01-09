RsnapshotWebmin
===============

Webmin Module for configuring Rsnapshot automatic backups

Home page: http://tbanelwebmin.free.fr/

Installation
============

- Open Webmin in a web browser, usually the address is https://localhost:10000/
- Go to Webmin > Webmin Configuration > Webmin Modules
- Check Third party module from and choose the rsnapshot entry.
- OR Check From ftp or http URL,
  and enter the url of the plug-in (either one):
  - http://tbanelwebmin.free.fr/rsnapshot-0.3.wbm.gz
  - https://github.com/tbanel/rsnapshotwebmin/releases/download/v0.3/rsnapshot-0.3.wbm.gz

When done, the module is accessible from System > Rsnapshot Backup.

You may also download the module
- here: http://tbanelwebmin.free.fr/rsnapshot-0.3.wbm.gz
- or here: https://github.com/tbanel/rsnapshotwebmin/releases/download/v0.3/rsnapshot-0.3.wbm.gz

License
=======

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at
your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

Author: © 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020; 2021, 2022 Thierry Banel <tbanelwebmin@free.fr>

Contributors (with permission):
  - Ken (ken at farville dot com)
  - Nico Kadel-Garcia (nkadel at gmail dot com)
  - ...and others

About Webmin
============

Webmin is an administration tool for Unix and Linux systems. 

It uses a standard web browser for its interface. 

It is made of plug-ins.

About Rsnapshot
===============

Rsnapshot is a backup utility for Unix and Linux systems. 

It creates "snapshots" of entire directories, thus keeping the state
of directories at intervals.

It does so in an efficient way: only changes from a snapshot to the
next use disk space.

Author
======

Thierry Banel, tbanelwebmin at free dot fr

Related works
=============

WebRsnapshot (http://dobrev.ws/projects/webrsnapshot) by Georgi Dobrev
is quite similar to the Webmin Rsnapshot module.
The main difference is that it works on it own, whereas the
Webmin Rsnapshot module is part of the Webmin system administrator.

Here is a tutorial
(http://ubuntupop.blogspot.fr/2014/04/install-rsnapshot-module-on-webmin.html)
by Fitri Aryani about installation of the module.

