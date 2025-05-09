# QGIS Sustaining Members Website
[![DPG Badge](https://img.shields.io/badge/Verified-DPG-3333AB?logo=data:image/svg%2bxml;base64,PHN2ZyB3aWR0aD0iMzEiIGhlaWdodD0iMzMiIHZpZXdCb3g9IjAgMCAzMSAzMyIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTE0LjIwMDggMjEuMzY3OEwxMC4xNzM2IDE4LjAxMjRMMTEuNTIxOSAxNi40MDAzTDEzLjk5MjggMTguNDU5TDE5LjYyNjkgMTIuMjExMUwyMS4xOTA5IDEzLjYxNkwxNC4yMDA4IDIxLjM2NzhaTTI0LjYyNDEgOS4zNTEyN0wyNC44MDcxIDMuMDcyOTdMMTguODgxIDUuMTg2NjJMMTUuMzMxNCAtMi4zMzA4MmUtMDVMMTEuNzgyMSA1LjE4NjYyTDUuODU2MDEgMy4wNzI5N0w2LjAzOTA2IDkuMzUxMjdMMCAxMS4xMTc3TDMuODQ1MjEgMTYuMDg5NUwwIDIxLjA2MTJMNi4wMzkwNiAyMi44Mjc3TDUuODU2MDEgMjkuMTA2TDExLjc4MjEgMjYuOTkyM0wxNS4zMzE0IDMyLjE3OUwxOC44ODEgMjYuOTkyM0wyNC44MDcxIDI5LjEwNkwyNC42MjQxIDIyLjgyNzdMMzAuNjYzMSAyMS4wNjEyTDI2LjgxNzYgMTYuMDg5NUwzMC42NjMxIDExLjExNzdMMjQuNjI0MSA5LjM1MTI3WiIgZmlsbD0id2hpdGUiLz4KPC9zdmc+Cg==)](https://blog.qgis.org/2025/02/08/qgis-recognized-as-digital-public-good/)

![image](https://github.com/user-attachments/assets/cfd5b563-0cb3-443f-b243-70a953b81180)


A django app for managing QGIS' sustaining members.

View a running instance at [https://members.qgis.org](https://members.qgis.org)


Note that whilst usable, Projecta is under continual development and not
yet feature complete.

The latest source code is available at 
[https://github.com/qgis/QGIS-Members-Website](https://github.com/qgis/QGIS-Members-Website).

* **Developers:** See our [developer guide](README-dev.md)
* **For production:** See our [deployment guide](README-docker.md)

## TODO: Update this README

## Key features

* Supports multiple projects
* Each project can have multiple software releases
* Each Release can have multiple entries explaining features related to it
* Entries can include text explaining the feature, an embedded video, an image
* Markdown is supported for entries
* Changelogs can be exported to RST for use in your sphinx project
* Sponsors can be managed for each project
* Various options for managing sponsors including sponsorship period and level
* Committees to organise groups of people in the project
* Votes that can be taken by members within the committee
* Disqus commenting


## Project activity

Story queue on Waffle:

* [![Stories in Ready](https://badge.waffle.io/kartoza/prj.app.svg?label=ready&title=Ready)](http://waffle.io/kartoza/prj.app) 
* [![Stories in In Progress](https://badge.waffle.io/kartoza/prj.app.svg?label=in%20progress&title=In%20Progress)](http://waffle.io/kartoza/prj.app)

[![Throughput Graph](https://graphs.waffle.io/kartoza/prj.app/throughput.svg)](https://waffle.io/kartoza/prj.app/metrics)

* Current test status master: [![Build Status](https://travis-ci.org/kartoza/prj.app.svg?branch=master)](https://travis-ci.org/kartoza/prj.app) and
[![Code Health](https://landscape.io/github/kartoza/prj.app/master/landscape.svg?style=flat)](https://landscape.io/github/kartoza/prj.app/master)

* Current test status develop: [![Build Status](https://travis-ci.org/kartoza/prj.app.svg?branch=develop)](https://travis-ci.org/kartoza/prj.app) and
[![Code Health](https://landscape.io/github/kartoza/prj.app/develop/landscape.svg?style=flat)](https://landscape.io/github/kartoza/prj.app/develop)

* Test coverage [![codecov](https://codecov.io/gh/kartoza/prj.app/branch/develop/graph/badge.svg)](https://codecov.io/gh/kartoza/prj.app)



## Quick Installation Guide

For deployment we use [docker](http://docker.com) so you need to have docker 
running on the host. Projecta is a django app so it will help if you have
some knowledge of running a django site.

```
git clone git://github.com/kartoza/projecta.git
cd projecta/deployment
cp btsync-db.env.EXAMPLE btsync-db.env
cp btsync-media.env.EXAMPLE btsync-media.env
cp .env.example .env
make build
make permissions
make web
# Wait a few seconds for the DB to start before to do the next command
make migrate
make collectstatic
```

If you need backups, put btsync keys in these files. If you don't need backups, 
you can let the default content.

So as to create your admin account:
```
make superuser
```

**intercom.io**

If you wish to make use of [intercom.io](https://www.intercom.io), include a
`private.py` file in `core.settings` with your `INTERCOM_APP_ID` as a string.
The necessary code snippet is already included in `base_with_sidebar.html`.

**google authentication**

In social auth to use the google authentication you need to go to:

https://console.developers.google.com/apis/credentials

Create and oath2 credential with these options:

Authorized redirect URIs

http://<your domain>/en/complete/google-oauth2/

Use the projecta admin panel to set up the google account with your id and
secret

**github authentication**

Create a developer key here:

https://github.com/settings/applications/new

Set the callback and site homepage url to the top of your site e.g.

http://localhost:61202

At http://localhost:61202/en/site-admin/socialaccount/socialapp/add/

Set the key and secret from the github key page.

**Backups**

If you wish to sync backups, you need to establish a read / write btsync 
key on your production server and run one or more btsync clients 
with a read only key.

```
cd deployment
cp btsync-media.env.EXAMPLE btsync-media.env
cp btsync-db.env.EXAMPLE btsync-db.env
```

Now edit the ``btsync-media.env`` and ``btsync-db.env`` files, including 
relevant SECRET and DEVICE settings.

## Participation


We work under the philosophy that stakeholders should have access to the
development and source code, and be able to participate in every level of the 
project - we invite comments, suggestions and contributions.  See
[our milestones list](https://github.com/kartoza/projecta/milestones) and
[our open issues list](https://github.com/kartoza/projecta/issues?page=1&state=open)
for known bugs and outstanding tasks. You can also chat live with our developers
and community members using the link below.

[![Join the chat at https://gitter.im/kartoza/projecta](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/kartoza/projecta?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)



## Credits

Projecta was funded and developed by [Kartoza.com](http://kartoza.com) and 
individual contributors.

## License

Projecta is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License version 3 (GPLv3) as
published by the Free Software Foundation.

The full GNU General Public License is available in LICENSE.txt or
http://www.gnu.org/licenses/gpl.html


## Disclaimer of Warranty (GPLv3)

There is no warranty for the program, to the extent permitted by
applicable law. Except when otherwise stated in writing the copyright
holders and/or other parties provide the program "as is" without warranty
of any kind, either expressed or implied, including, but not limited to,
the implied warranties of merchantability and fitness for a particular
purpose. The entire risk as to the quality and performance of the program
is with you. Should the program prove defective, you assume the cost of
all necessary servicing, repair or correction.

## Thank you

Thank you to the individual contributors who have helped to build projecta:

* Tim Sutton (Lead developer): tim@kartoza.com
* Dražen Odobašić : dodobas@geoinfo.geof.hr
* George Irwin : github@grvhi.com
* Ismail Sunni : imajimatika@gmail.com
* Richard Duivenvoorde : richard@duif.net
* Rischan Mafrur : @rischanlab
* Etienne Trimaille : @gustry
* Anita Hapsari : @ann26
* Muhammad Yarjuna Rohmat : @myarjunar

