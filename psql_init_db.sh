#!/bin/bash
##
## psql_init_db.sh
##
## This shell script helps to create and initialize a postgres 9.5 db for rapni
##
## copyright: (c) 2016 Internet Archive.
##    author: Giovanni Damiola <gio@archive.org>
##


echo "This script will create a PostgreSQL user and db for rapni.py"

#echo "Database username"
#read psqluser
#echo "Database password"
#read psqlpass
#echo "Database name"
#read psqldb

psqluser='rapni'
psqlpass='rapni'
psqldb='rapni'

sudo printf "DROP DATABASE IF EXISTS $psqldb;\nDROP ROLE IF EXISTS $psqluser;\n" > rapni_initialize_db.sql
sudo printf "CREATE USER $psqluser WITH PASSWORD '$psqlpass';\nCREATE DATABASE $psqldb WITH OWNER $psqluser;" >> rapni_initialize_db.sql
sudo -u postgres psql -f rapni_initialize_db.sql

echo 'Done!'
