"""
config.py

the main RAPNI configuration file

:copyright: (c) 2016 Internet Archive.
:   author: Giovanni Damiola <gio@archive.org>
"""

## log and debug
DEBUG                        = True
TESTING                      = False

## server configuration
SERVER_PORT                  = 5000
SERVER_HOST                  = '127.0.0.1'

## default number results
DEFAULT_RESULTS_NUM          = 100

## postgresql
PSQL_HOST                    = 'localhost'
PSQL_PORT                    = 5432
PSQL_USER                    = 'rapni'
PSQL_PASSWD                  = 'rapni'
PSQL_DB                      = 'rapni'
PSQL_URI                     = "postgresql://{0}:{1}@{2}:{3}/{4}".format(PSQL_USER, PSQL_PASSWD, PSQL_HOST, PSQL_PORT, PSQL_DB)

## CORS
ALLOWED_CORS_DOMAINS         = [ "https://localhost", "https://localhost" ]

## AUTH TOKEN
AUTH_TOKEN                   = 'fc6add639e80f76e047f642fe6952168'
