=======
C3S ADO
=======

    *Much Ado About Nothing* by William Shakespeare

Ado is a collection of services which are helpful when setting up a collecting
society.


Overview
========
The ado setup creates and maintains `Docker <http://docs.docker.com>`
containers for development and also production use.
`Docker-compose <https://docs.docker.com/compose/>`, - vagrant for docker containers, - is used as a creator
and configurator for the needed Docker container setups:

    1. Postgres database (db)
       A database with name ``c3s`` is created automatically.
       Demo data included.
    2. Web portal service including Tryton and Pyramid (portal)
       All Tryton and Pyramid dependencies installed
    3. Tryton service (tryton)



Requirements
============
A Linux or OS X system, `docker <http://docs.docker.com/installation>`,
`docker-compose  <https://docs.docker.com/compose/install/>`
and `git <http://git-scm.com/downloads>`.


Setup
=====
Clone this repository into your working space::

    $ cd WORKING/SPACE
    $ git clone git@sparkle.c3s.cc:c3s.ado.git

All setup and maintenance tasks are done in the root path of the
``c3s.ado/`` repository.

Update the environment, clone/pull development repositories::

    $ cd c3s.ado
    $ ./update

Build docker containers::

    $ docker-compose build

The initial build of the containers will take some time.
Later builds will take less time.

Adjust environment files for containers, if neccessary. Sane defaults for
a development setup are given:

    * ``./portal.env``
    * ``./api.env``

Change the password for the *admin* user in
``ado/etc/trytonpassfile``

Start containers::

    $ docker-compose up

This starts all *ado* service containers.


Clients
=======
Web
---
The number of *portal* services is implemented scalable.
Because of this it is not possible to hard code the external port number of
a service.
So all services use *random external ports on the host system*.
The tool `nginx-proxy<https://github.com/jwilder/nginx-proxy>` is used as a
reverse proxy and load-balancer to the *portal* services host on *port 81*.

.. note: To connect a client to a particular service, it is
    needed to find out the hosta nd the port of the service.
    Use the script ``c3s.ado/show_external_urls`` or ``docker-compose ps``
    to find the port of a particular service.

Connecting the portal, point your browser to::
    http://0.0.0.0.xip.io:81

Connecting the api, point your browser to::
    http://api.0.0.0.0.xip.io:81

Connecting a specific instance of the portal service, point your browser to::
    http://localhost:<random external port on host system>/login

Tryton
------
To connect to trytond you can use one of the several Tryton client
applications or APIs.
For back-office use of the application the Gtk2 based Tryton client is
recommended.

Install the client application with the name *tryton* or *tryton-client* in
Version 3.4.x from your Linux distribution.
You can also use the source, OS X, or Windows packages or binaries found here:
`<http://www.tryton.org/download.html>`

On the host system connect to::

    server: localhost
    port: 8000
    database: c3s
    user: admin
    password: admin

.. note:: Tryton server and the client are required to have the same version
    branch (actual 3.4.x).


Using containers
================
Services
--------
For development purposes it is convenient to have the possibility to debug the
running code.
To start only the necessary services for developing a service
use e.g::

    $ docker-compose run --service-ports portal ado-do deploy-portal
    $ docker-compose run --service-ports api ado-do deploy-api
    $ docker-compose run --service-ports portal ado-do deploy-tryton c3s


The portal service is started with ``ado-do`` inside a portal container.
The tryton service can be started with::

    $ docker-compose run --service-ports tryton ado-do deploy-tryton c3s

The flag ``service-ports`` runs the container and all its dependecies
with the service's ports enabled and mapped to the host.
For development is the benefit of starting a service with
``docker-compose run --service-ports <service>`` vs ``docker-compose up``
the possibility to communicate with a debugger like pdb.

A similar topic is to start a shell in a container.
To manually examine the operating system of a container, just run a shell in
the container::

    $ docker-compose run portal /bin/bash

.. warning:: Manual changes are not persisted when closing a container.
    All changes are reset.

.. note:: The console is always opend in a freshly build of the service and
    does not connect to a running container. To enter a running container use
    ``docker exec``. See below for further instructions.

*Ado-do* is a command line tool to setup and maintain services in a container.
To start the ``ado-do`` command from inside a container the
``docker-compose run ado`` must be removed from the following examples.

Get acquainted with ``ado-do`` a command driven tool which performs tasks on
container start::

    $ docker-compose run portal ado-do --help
    $ docker-compose run portal ado-do COMMAND --help


Database
--------
Update all modules in an existing database with name DATABASE_NAME::

    $ docker-compose run tryton ado-do update DATABASE_NAME


Update specific modules in an existing database::

    $ docker-compose run tryton ado-do update  \
        -m MODULE_NAME1[,MODULE_NAME2,…] DATABASE_NAME

E.g.::

    $ docker-compose run tryton ado-do update  \
        -m party,account,collecting_society c3s


Examine and edit a database, use::

    $ docker-compose run tryton ado-do db-psql DATABASE_NAME

Backup a database::

    $ docker-compose run tryton ado-do db-backup DATABASE_NAME  \
        > `date +%F.%T`_DATABASE_NAME.backup

Delete a database::

    $ docker-compose run tryton ado-do db-delete DATABASE_NAME


Create a new database::

    $ docker-compose run tryton ado-do db-create DATABASE_NAME

Re-new a database::

    $ docker-compose run tryton ado-do db-delete DATABASE_NAME
    $ docker-compose run tryton ado-do db-demo-setup DATABASE_NAME

The ``ado-do db-demo-setup`` command combines the following two steps::

    $ # docker-compose run tryton ado-do db-create DATABASE_NAME
    $ # docker-compose run tryton ado-do update DATABASE_NAME


Service Scaling
---------------
To scale increasing load it is possible to start more service containers on
demand::

    $ docker-compose scale portal=2 tryton=3 db=1

To scale decreasing load it is possible to stop service containers on demand::

    $ docker-compose scale tryton=2

Lookup all host ports in use::

    $ /path/to/c3s.ado/show_external_urls

… or use ``docker-compose ps`` as an alternative.

Lookup a specific host port in use::

    $ docker-compose --index=1 port tryton 8000

.. note:: This command has a fixed but not merged and released bug:
    https://github.com/docker/compose/issues/667


Integration Tests
-----------------
To run tests in the tryton container use::

    $ docker-compose run tryton sh -c \
          'ado-do pip-install tryton \
          && export DB_NAME=:memory: \
          && python /ado/src/trytond/trytond/tests/run-tests.py'

To run the demo-setup again, use::

    $ docker-compose run tryton sh -c \
          'ado-do pip-install tryton \
          && python -m doctest -v etc/scenario_master_data.txt'


Maintenance After c3s.ado Update
--------------------------------
Some changes in the container setup require a rebuild of the whole system.
Best is to move the actual ``c3s.ado`` directory to another name and
make a fresh clone of the ``c3s.ado`` repository.

Update the environment as usual::

    $ cd c3s.ado
    $ ./update

Build containers, this time without a cache::

    $ docker-compose build --no-cache

Start containers::

    $ docker-compose up


Deployment
==========
Monitoring
----------
To monitor all running containers use::

    $ watch ./monitor

.. note:: The monitoring abilities are limted to system and user cpu and
    rss+cache size. The most informative metrics to use for monitoring
    are a moving target.

Development
===========
The general Python requirements are provided by default Debian packages from
Jessie (actual testing) if available, otherwise from PyPI.
Packages under development are located in ``ado/src`` and can be edited on the
host system, outside the containers.
For developer convenience all Tryton modules use a git mirror of the upstream
Tryton repositories.
For this setup the Tryton release branch 3.4 is used.

Architecture
------------
This repository is build by the following files and directories::

    ├── ado  # This directory is mapped into portal and tryton container
    │   ├── ado-do  # Maintenance Utility for containers
    │   ├── etc
    │   │   ├── requirements-portal.txt  # Pip requirements for portal service
    │   │   ├── requirements-tryton.txt  # Pip requirements for Tryton service
    │   │   ├── scenario_master_data.txt # Demo data script
    │   │   ├── trytond.conf  # Configuration file for Tryton service
    │   │   └── trytonpassfile  # Password file for Tryton admin user
    │   ├── src  # Source repositories, edit here
    │   │   ├── account
    │   │   ├── account_invoice
    │   │   ├── ...
    │   └── var  # upload directory for tryton webdav service
    │       └── lib ...
    ├── CHANGELOG
    ├── config.py  # Configuration for paths and reporitories
    ├── Dockerfiles  # Definition of service container images
    │   ├── portal ...
    │   └── tryton ...
    ├── docker-compose.yml  # docker-compose configuration
    ├── postgresql-data ...  # postgresql database data files
    ├── README.rst  #*this file*
    ├── show_external_urls  # helper script to show used external urls
    └── update  # Update script for repositories and file structure

Packages and Debs
-----------------
This setup maintains three levels of package inclusion:

    1. Debian packages
    2. Python packages installed with pip
    3. Source repositories for development purposes

Source packages for the development are available as git repositories are
stored in ``config.py`` in variable ``repositories``::

    (
        git repository url or None.
        git clone option, required if repository is given.
        relative path to create or clone.
    ),

These packages are cloned or updated with the ``./update`` command and must
be pip installable.
To install a source repository package in a container, it is be declared in
*one* of the ``ado/etc/requirements*.txt`` files.

.. note:: The ``requirements-portal.txt`` inherits the
    ``requirements-tryton.txt``.
.. note:: The ``config.py`` can be used to create empty directories, too.

Debian and Python packages are included in one of the ``Dockerfiles``:

    * tryton
    * portal

.. note:: Add source repository packages only when they are realy needed for
    development.

Remove Database
---------------
The database files are stored in ``postgresql-data``.
To rebuild a new database use the following pattern::

    $ docker-compose stop db
    $ docker-compose rm db
    $ sudo rm -rf postgresql-data/
    $ mkdir postgresql-data

.. warning:: All data in this database will be deleted!


Problems
========
Couldn't connect to Docker daemon
---------------------------------
Docker-compose cannot start container <id> port has already been allocated
--------------------------------------------------------------------------
If docker fails to start and you get messages like this:
"Couldn't connect to Docker daemon at http+unix://var/run/docker.sock
[...]" or "docker-compose cannot start container <docker id> port has already
been allocated"

1. Check if the docker service is started::

    $ /etc/init.d/docker[.io] stop
    $ /etc/init.d/docker[.io] start

2. Check if any user of docker is member of group ``docker``::

    $ login
    $ groups | grep docker

Bad Fingerprint
---------------
If the Tryton client already connected the *tryton*-container, the fingerprint
check could restrict the login with the message: Bad Fingerprint!

That means the fingerprint of the server certificate changed.
In production use, the ``Bad fingerprint`` alert is a sign that someone
could try to *fish* your login credentials with another server responding your
client.
Ask the server administrator if the certificate is changed.

Close the Tryton client.
Check the problematic host entry in ``~/.config/tryton/3.4/known_hosts``.
Add a new fingerprint provided by the server administrator or
simply remove the whole file, if the setup is not in production use::

    rm ~/.config/tryton/3.4/known_hosts

Testing
-------
For manual execution of nosetests, you need to start the container:

* docker-compose run portal bash
* ado-do pip-install portal

execute nosetest:

* nosetests -v --nologcapture /ado/src/collecting_society.portal/collecting_society_portal/tests/nose-test-01.py

Engine Room
-----------
This is a collection of docker internals.
Good to have but seldom useful.

Show running container (docker-compose level), e.g. ::

    $ docker-compose ps
        Name                 Command                      State    Ports
    ---------------------------------------------------------------------------
    c3sadointernal_db_1      /docker-entrypoint.sh postgres  Up  5432/tcp
    c3sadointernal_portal_1  ado-do deploy-portal            Up  6543->6543/tcp
    c3sadointernal_tryton_1  ado-do deploy-tryton c3s        Up  8000->8000/tcp


Use docker help::

    $ docker help

Show running container (docker level)::

    $ docker ps

Enter a running container by id (Docker>=1.3;Kernel>3.8)::

    $ docker exec -it <container-id> bash


.. note:: The docker containers are usually stored under ``/var/lib/docker``
    and can occupy some gigabyte diskspace.


Docker is memory intensive. To Stop and remove all containers use::

    $ docker stop $(docker ps -a -q)
    $ docker rm $(docker ps -a -q)

Remove images ::

    $ docker rmi $(docker images -f "dangling=true" -q)

In case you need disk space, remove all local cached images::

    $ docker rmi $(docker images -q)


Copyright / License
===================
For infos on copyright and licenses, see ``./COPYRIGHT.rst``


References
==========
    * http://crosbymichael.com/dockerfile-best-practices.html
    * http://crosbymichael.com/dockerfile-best-practices-take-2.html
    * https://crosbymichael.com/advanced-docker-volumes.html
    * http://blog.jacius.info/git-submodule-cheat-sheet/
