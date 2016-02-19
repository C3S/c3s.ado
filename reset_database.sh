#!/bin/bash

echo "====================================================================="
echo "====================================================================="
echo "= this script stops, destroys, rebuilds, restarts the c3s.ado setup ="
echo "====================================================================="
echo `date +%Y-%m-%d:%H:%M:%S`

cd /srv/web/alpha.adore-music.com/c3s.ado

# stop docker containers
echo -e "\n== stop docker containers"
/usr/local/bin/docker-compose stop

# delete database
echo -e "\n== delete database"
/usr/local/bin/docker-compose run portal ado-do db-delete c3s
echo $?
echo "0 means success, 1 and above mean failure!"

# re-create database
echo -e "\n== re-create database"
/usr/local/bin/docker-compose run tryton ado-do db-demo-setup c3s &> /dev/null
echo $?
echo "0 means success, 1 and above mean failure!"

# start docker containers
echo -e "\n== start docker containers"
/usr/local/bin/docker-compose up -d

echo `date +%Y-%m-%d:%H:%M:%S`
echo "====================================================================="
echo "====================================================================="