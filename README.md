# RAPNI

Rapni is a basic RESTful API to use PostgreSQL as JSON documents NoSQL store.

## Author
- Giovanni Damiola - <gio@archive.org>

## Requirements

    python python-dev
    postgres 9.5
    postgresql-server-dev-9.5

about how to install postgresql9.5 check the link: https://git.archive.org/snippets/12


## Install PostgreSQL v9.5 for ubuntu

### Install and configure the ubuntu repository

    sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'
    wget -q https://www.postgresql.org/media/keys/ACCC4CF8.asc -O - | sudo apt-key add -

### Install the packages

    sudo apt-get update
    sudo apt-get install postgresql postgresql-contrib  postgresql-server-dev-9.5


## Install Rapni

To start, first, **clone** the repository:

    git clone https://github.com/gdamdam/rapni.git
    cd rapni

Before installing the python **requirements** it"s a good idea to use a *virtualenv* :

    virtualenv -p python2.7 venv
    source ./venv/bin/activate

Install then the requirements:

    pip install -r requirements.txt

Initialize and create the **database**

    /bin/bash psql_init_db.sh

**Configure** the app properties:

    vim config.py

You can **test** the app:

    python tests.py

**Launch** the service

    python rapni.py



## Quickstart

**show_all**:

    curl http://host:5000/docs

**get_doc**:

    curl http://host:5000/docs/ID_docs

**insert**:

    curl http://host:5000/docs/ID_docs -X POST -H "Content-Type: application/json" -H "Authorization: AUTH_TOKEN" -d "JSON_DOCUMENT"

**udpate**:

    curl http://host:5000/docs/ID_docs -X PUT -H "Content-Type: application/json" -H "Authorization: AUTH_TOKEN" -d "JSON_DOCUMENT"

**delete**:
    curl http://host:5000/docs/ID_docs -X DELETE -H "Authorization: AUTH_TOKEN"


There is also the entry point *events*, it is a little different:

    curl http://host:5000/events -X POST  -H "Content-Type: application/json" -H "Authorization: AUTH_TOKEN" -d "JSON_DOCUMENT"

the JSON_DOCUMENT must contain a key = "target".

To **view all** the events recorded for a target:

    curl http://host:5000/events/TARGET_ID

**get all** the documents for a LOCATION_ID:

    curl http://host:5000/docs/LOCATION_ID/documents


# License

    RAPNI: a basic RESTful API to use PostgreSQL as JSON documents NoSQL store.

    Copyright (C) 2016 Internet Archive

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses>
