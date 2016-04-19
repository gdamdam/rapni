"""
rapni.py

Rapni is a basic RESTful API to use PostgreSQL as JSON documents NoSQL store.

:copyright: (C) 2016 Internet Archive.
:   author: Giovanni Damiola <gio@archive.org>
"""

__author__     = "Giovanni Damiola"
__copyright__  = "Copyright 2016, Internet Archive"
__email__      = "gio@archive.org"
__maintainer__ = "Giovanni Damiola"
__version__    = "v0.1"

### Imports
from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort
from flask.ext.httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from flask.ext.cors import CORS

import config
import json
import re
import sys
import logging
from db_tools import db_connector
from db_tools import database

# initializing the db, the tables will be created as described in the db_model
database.init_db()

## initializing logger
log = logging.getLogger('rapni')

log.setLevel(logging.DEBUG) if config.DEBUG else log.setLevel(logging.INFO)
fh = logging.StreamHandler(sys.stdout)
fh.setLevel(logging.DEBUG) if config.DEBUG else fh.setLevel(logging.INFO)
formatter=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
log.addHandler(fh)

## create object db_connector
db = db_connector.DbConnector('rapni')

### Some initialization
app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": config.ALLOWED_CORS_DOMAINS}})
auth = HTTPBasicAuth()

parser = reqparse.RequestParser()
parser.add_argument('data', type=str)

## RESTful APP
##

## This is a generic resource class for this API
## providing the main method behaviour
##
class IdsResource(Resource):
    """ The generic resource class for the API:
    /resource/<identifier>
    It provides the main behaviour for all the REST methods.
    """

    def __init__(self, collection):
        """Initializes the class. The COLLECTION value will be used to Define
        the target table of all the queries used in the queries.
        """
        self.COLLECTION = collection

    def validate(func):
        """A decorator function to validate the identifier input."""
        def func_wrapper(self, identifier):
            if re.match(r'^[A-Za-z0-9._+-]{2,100}$',identifier):
                return func(self,identifier)
            else:
                res_msg = "ERROR - The identifier {0} is not valid. Alphanumeric characters only plus [._+-] from 2 to 30 chars long.".format(identifier)
                log.info(res_msg)
                return res_msg, 406
        return func_wrapper

    @auth.verify_password
    def verify_password(username, password):
        """Define the method used to verify the authentication/authorization
        """
        token = request.headers.get('Authorization')
        if token == config.AUTH_TOKEN:
            return True
        else:
            log.info('Authorization failure')
            return False

    @validate
    def get(self,identifier):
        """ List all the metadata for the target object identifier.

        arguments:
            identifier -- the object identifier

        returns:
            a JSON document with all the results
        """
        try:
            res = db.get_doc_id(self.COLLECTION, identifier)
            return res, 200
        except:
            res_msg = "NOT FOUND - Document {0} does not exist.".format(identifier)
            return res_msg, 404

    @validate
    @auth.login_required
    def put(self,identifier):
        """ Updates the document content of an object with the JSON document in the data.
        Only the changes in the attributes will be updated.

        arguments:
            identifier -- the object identifier

        returns:
            the status code of the response (200, 404, 406)
        """
        if not (db.exists(self.COLLECTION, identifier)):
            abort(404, message = "NOT FOUND - The element {0} does not exists".format(identifier))
        else:
            data = request.json
            if data != '':
                record = db.update(self.COLLECTION, data, identifier)
                res_msg = "OK - Record {0} succesfully updated.".format(identifier)
                log.info(res_msg)
                return res_msg, 200
            else:
                res_msg = "ERROR: Empty payload in the POST request.\n Don't forget the header Content-Type: application/json in the request"
                log.info(res_msg)
                return res_msg, 406

    @validate
    @auth.login_required
    def post(self,identifier):
        """ Creates an entry for an object containing the JSON document in the data.

        arguments:
            identifier -- the object identifier

        returns:
            the status code of the response (201, 406, 409)
        """
        if db.exists(self.COLLECTION, identifier):
            res_msg = "CONFLICT - The element {0} already exists".format(identifier)
            log.info(res_msg)
            abort(409, message = res_msg)
        else:
            data = request.json
            if data != None:
                record = db.insert(self.COLLECTION, data, identifier)
                res_msg = "OK - Record {0} succesfully created.".format(identifier)
                log.info(res_msg)
                return res_msg, 201
            else:
                res_msg = "ERROR: Empty payload in the POST request. Don't forget the header Content-Type: application/json in the request"
                log.info(res_msg)
                return res_msg, 406


    @validate
    @auth.login_required
    def delete(self,identifier):
        """ Delete the entry for an object.

        arguments:
            identifier -- the object identifier

        returns:
            the status code of the response (200, 404)
        """
        if not (db.exists(self.COLLECTION, identifier)):
            res_msg = "NOT FOUND - The element {0} does not exists".format(identifier)
            log.info(res_msg)
            abort(404, message = res_msg)
        else:
            res = db.remove(self.COLLECTION, identifier)
            res_msg = "OK - Record {0} DELETED.".format(identifier)
            log.info(res_msg)
            return res_msg, 200





class IdsViewResource(Resource):
    """ The generic display resource class for the API:
    /resource/
    It provides the main behaviour for all the REST methods.
    """

    def get(self):
        """ return all resource entries metadata with pagination

            /resource?limit=LIMIT&offset=OFFSET
        """
        ## check if there is a limit parameter in the uri
        if request.args.get('limit'):
            limit = request.args.get('limit')
        else:
            limit = config.DEFAULT_RESULTS_NUM
        ## check if there is a limit offset in the uri
        if request.args.get('offset'):
            offset = request.args.get('offset')
        else:
            offset = 0

        res= db.get_all(collection=self.COLLECTION, result_num=limit, offset=offset)
        rres = {}
        for r in res:
            rres[str(r.identifier)] = r.document
            rres[str(r.identifier)]['created_on'] = str(r.created_on)
            rres[str(r.identifier)]['updated_on'] = str(r.updated_on)
        return rres, 200

    def post(self):
        """ Method not allowed
        """
        res_msg = "ERROR - POST method is not allowed."
        return res_msg, 405

    def put(self):
        """ Method not allowed
        """
        res_msg = "ERROR - PUT method is not allowed."
        return res_msg, 405

    def delete(self):
        """ Method not allowed
        """
        res_msg = "ERROR - DELETE method is not allowed."
        return res_msg, 405


class IdsResourceDetails(Resource):
    """ The generic display details class for the API:
    /resource/<identifier>/resource_type
    It provides the main behaviour for all the REST methods.
    """

    def __init__(self,target_attrib):
        """Initializes the class. The TARGET_DETAIL_ATTRIB is the attributhe key
        used in the WHERE query statement.
        """
        selt.TARGET_DETAIL_ATTRIB = target_attrib

    def get(self, identifier, resource):
        """ returns all resource entries metadata with a specific attrib value.
            /resource/<identifier>/resource_type

            arguments:
                identifier -- the object identifier
                resource -- the resource type we want to retrieve (books)

            returns:
                a JSON document with the reults and
                the status code of the response (200, 406)
        """
        if request.args.get('limit'):
            limit = request.args.get('limit')
        else:
            limit = config.DEFAULT_RESULTS_NUM
        ## check if there is a limit offset in the uri
        if request.args.get('offset'):
            offset = request.args.get('offset')
        else:
            offset = 0

        if resource == 'documents':
            res = db.get_using_attrib("Documents", self.TARGET_DETAIL_ATTRIB, identifier, limit, offset)
            rres = {}
            for r in res:
                rres[r.identifier] = r.document
                rres[r.identifier]['created_on'] = str(r.created_on)
                rres[r.identifier]['updated_on'] = str(r.updated_on)
            return rres, 200
        if resource == 'events':
            res = db.get_using_attrib("events", self.TARGET_DETAIL_ATTRIB, identifier, limit, offset)
            rres = {}
            for r in res:
                rres[r.identifier] = r.document
                rres[r.identifier]['created_on'] = str(r.created_on)
                rres[r.identifier]['updated_on'] = str(r.updated_on)
            return rres, 200
        else:
            res_msg = "ERROR - {0} resource is not allowed.".format(resource)
            return res_msg, 406

    def post(self):
        """ Method not allowed
        """
        res_msg = "ERROR - POST method is not allowed."
        return res_msg, 405

    def put(self):
        """ Method not allowed
        """
        res_msg = "ERROR - PUT method is not allowed."
        return res_msg, 405

    def delete(self):
        """ Method not allowed
        """
        res_msg = "ERROR - DELETE method is not allowed."
        return res_msg, 405


## DOCUMENTS
class IdsDocuments(IdsResource):
    def __init__(self):
        self.COLLECTION = "Documents"

class IdsDocumentsView(IdsViewResource):
    def __init__(self):
        self.COLLECTION = "Documents"

class IdsDocumentsDetails(IdsResourceDetails):
    def __init__(self):
        self.COLLECTION = "Documents"
        self.TARGET_DETAIL_ATTRIB = 'location'




class IdsEventsView(IdsResource):
    """ Class defining the View for the events contents.
    """
    def __init__(self):
        self.COLLECTION = "Events"

    def get(self):
        """ returns all events entries metadata.
            /events/

            returns:
                a JSON object with all the results.
        """

        ## check if there is a limit parameter in the uri
        if request.args.get('limit'):
            limit = request.args.get('limit')
        else:
            limit = config.DEFAULT_RESULTS_NUM
        ## check if there is a limit offset in the uri
        if request.args.get('offset'):
            offset = request.args.get('offset')
        else:
            offset = 0
        res = db.get_all_using_attrib(self.COLLECTION, 'target', result_num=limit, offset=offset)
        rres = {}
        for r in res:
            rres['{n:011d}'.format(n=r.identifier)] = r.document
            rres['{n:011d}'.format(n=r.identifier)]['created_on'] = str(r.created_on)
            rres['{n:011d}'.format(n=r.identifier)]['updated_on'] = str(r.updated_on)
        return rres, 200


    @auth.login_required
    def post(self):
        """ Creates an entry for an event object containing the JSON document in the data.
        The entries are added with an auto-increment id.
        The event is also parsed and processed, creating or updating all the other docs.

        returns:
            the status code of the response (201, 406)
        """
        data = request.json
        if data != None:
            ## TODO a better data schema validation
            ## and better error msg than e
            record = db.auto_add(self.COLLECTION, data)
            log.info('Event recorded.')
            res_msg = 'OK event recorded.'
            return res_msg, 201
        else:
            res_msg = "ERROR: Empty payload in the POST request. Don't forget the header Content-Type: application/json in the request"
            log.info(res_msg)
            return res_msg, 406



class IdsEvents(IdsViewResource):
    def __init__(self):
        self.COLLECTION = "Events"

    def get(self,identifier):
        """ returns all events entries metadata for a specific object identifier.

            arguments:
                identifier -- the object identifier

            returns:
                a JSON document with the reults and
                the status code of the response (200)
        """
        res = db.get_using_attrib(self.COLLECTION, 'target', identifier)
        rres = {}
        for r in res:
            rres['event-'+str(r.identifier)] = r.document
            rres['event-'+str(r.identifier)]['created_on'] = str(r.created_on)
            rres['event-'+str(r.identifier)]['updated_on'] = str(r.updated_on)
        return rres, 200


class IdsHello(Resource):
    """Main class for the wellcome resource.
    It provides version and a short messqge.
    """
    def get(self):
        res = json.loads('{"msg":"hello, welcome","version":"'+__version__+'"}')
        return res


@app.teardown_appcontext
def shutdown_session(exception=None):
    """ teardown_appcontect, destroy db_session when necessary
    """
    database.db_session.remove()


### initizing the api resources
api.add_resource(IdsDocuments, '/docs/<string:identifier>')
api.add_resource(IdsDocumentsView, '/docs')
api.add_resource(IdsDocumentsDetails, '/docs/<string:identifier>/<string:resource>')

api.add_resource(IdsEvents, '/events/<string:identifier>')
api.add_resource(IdsEventsView, '/events')

api.add_resource(IdsHello, '/')



def main():
    '''main function managing the setup and the server launch'''
    server_debug = config.DEBUG
    server_host = config.SERVER_HOST
    server_port = config.SERVER_PORT
    log.info('Starting {0} server {1}:{2}'.format(__file__, server_host, server_port))
    app.run(debug=server_debug, host=server_host, port=server_port)




if __name__ == '__main__':
    main()
