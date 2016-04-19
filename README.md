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


## Install

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
<pre>
    curl http://host:5000/docs
</pre>

**get_doc**:
<pre>
    curl http://host:5000/docs/ID_docs
</pre>

**insert**:
<pre>
    curl http://host:5000/docs/ID_docs -X POST -H "Content-Type: application/json" -H "Authorization: AUTH_TOKEN" -d "JSON_DOCUMENT"
</pre>

**udpate**:
<pre>
    curl http://host:5000/docs/ID_docs -X PUT -H "Content-Type: application/json" -H "Authorization: AUTH_TOKEN" -d "JSON_DOCUMENT"
</pre>

**delete**:
<pre>
    curl http://host:5000/docs/ID_docs -X DELETE -H "Authorization: AUTH_TOKEN"
</pre>


There is also the entry point *events*, it is a little different:

<pre>
    curl http://host:5000/events -X POST  -H "Content-Type: application/json" -H "Authorization: AUTH_TOKEN" -d "JSON_DOCUMENT"
</pre>

the JSON_DOCUMENT must contain a key = "target".

To **view all** the events recorded for a target:

<pre>
    curl http://host:5000/events/TARGET_ID
</pre>

**get all** the documents for a LOCATION_ID:

<pre>
    curl http://host:5000/docs/LOCATION_ID/documents
</pre>
