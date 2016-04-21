#
# db_connector.py
#
# Copyright (C) 2016 Internet Archive
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
db_connector.py

a simple NoSQL db connector using Postgresql tables with JSON documents columns.

the collection argument refers to the db_mode.py classes.

:copyright: (c) 2016 Internet Archive.
:   author: Giovanni Damiola <gio@archive.org>
"""

import sqlalchemy
import json
import logging
from database import db_session
import db_model as db


class DbConnector():
    DEFAULT_LOG_SERVICE_NAME = 'db-connector'
    DEFAULT_LOG_DEBUG = False

    def __init__(self, log_service_name=DEFAULT_LOG_SERVICE_NAME, log_debug=DEFAULT_LOG_DEBUG):
        self.log                      = logging.getLogger(log_service_name+'.db-connector')
        self.log.setLevel(logging.DEBUG) if log_debug else self.log.setLevel(logging.INFO)
        self.handler                  = logging.StreamHandler()
        self.handler.setLevel(logging.DEBUG) if log_debug else self.handler.setLevel(logging.INFO)
        self.formatter                = logging.Formatter('%(asctime)s [%(process)s] [%(name)s] [%(levelname)s] %(message)s')
        self.handler.setFormatter(self.formatter)
        self.log.addHandler(self.handler)


    def insert(self, collection, document, identifier):
        """ insert document into a collection

            arguments:
                identifier -- the identifier of the item we want to update
                collection -- string name of the collection (or table)
                document -- the document in JSON format to be inserted

            returns:
                the record_id
        """
        # instancing a class dynimically
        table_ = getattr(db, collection)
        entry = table_(identifier, document)
        try:
            db_session.add(entry)
            res = db_session.commit()
            self.log.debug("New identifier: {0} succesfully inserted.".format(identifier))
            return True
        except Exception, e:
            self.log.error("database commmit error: {0}").format(e)
            return False


    def auto_add(self, collection, document):
        """ insert a document in an auto increment table

            arguments:
                collection -- string name of the collection (or table)
                document -- the document in JSON format to be inserted

            returns:
                the record_id
        """
        table_ = getattr(db, collection)
        entry = table_(document)
        try:
            db_session.add(entry)
            res = db_session.commit()
            self.log.debug("New event")
            return True
        except Exception, e:
            self.log.error("database commmit error: {0}".format(e))
            return False



    def update(self, collection, document, identifier):
        """ update the content of an existing document
        the document is updated merging the two documents

            arguments:
                identifier -- the identifier of the item we want to update
                collection -- string name of the collection (or table)
                document -- the document in JSON format to be inserted

            returns:
                True/False
        """

        table_ = getattr(db, collection)
        try:
            old = db_session.query(table_).filter(table_.identifier == identifier).one()
            new_document = old.document.copy()
            new_document.update(document)
            db_session.query(table_).filter(table_.identifier==identifier).update({"document":new_document})
            self.log.debug("item {0} updated".format(identifier))
            res = db_session.commit()
            return True
        except Exception, e:
            self.log.error("database update error: {0}".format(e))
            return False


    def remove(self, collection, identifier):
        """ remove a document from a collection

            arguments:
                identifier -- the identifier of the item we want to update
                collection -- string name of the collection (or table)

            returns:
                True/False
        """
        table_ = getattr(db, collection)
        try:
            db_session.query(table_).filter(table_.identifier==identifier).delete()
            res = db_session.commit()
            self.log.debug("Item {0} removed.".format(identifier))
            return True
        except Exception, e:
            self.log.error("database remove error: {0}".format(e))
            return False


    def get_doc_id(self, collection, identifier):
        """ get the content of a document in a collection

            arguments:
                identifier -- the identifier of the item we want to update
                collection -- string name of the collection (or table)

            return:
                a json with the document
        """
        table_ = getattr(db, collection)
        uu = db_session.query(table_).filter(table_.identifier == identifier).one()
        res = {}
        res['updated_on'] = str(uu.updated_on)
        res['created_on'] = str(uu.created_on)
        res.update(uu.document)
        return res


    def get_docs_obj(self, collection, object_identifier):
        """ get the content of a document in a collection

            arguments:
                collection -- string name of the collection (or table)
                object_identifier -- the identifier of the object we want to show the tasks

            return:
                a list of tasks
        """
        table_ = getattr(db, collection)
        uu = db_session.query(table_).filter(table_.object_identifier == object_identifier).all()
        return uu


    def get_all(self, collection, result_num=100, offset=0):
        """ get content of a collection

            arguments:
                collection -- name of the collection (or table), string
                result_num -- the number of results returned, int

            returns:
                a list with all the results.
        """
        table_ = getattr(db, collection)
        all_res = db_session.query(table_).order_by(sqlalchemy.desc(table_.updated_on)).limit(result_num).offset(offset)
        res = []
        for vv in all_res:
            res.append(vv)
        return res


    def get_using_attrib(self, collection, attrib_key, attrib_value, result_num=100, offset=0):
        """ get raws though attribute value

            arguments:
                collection -- name of the collection (or table), string
                attrib_key --
                attrib_value --

            returns:
                a list with all the results.
        """
        table_ = getattr(db, collection)
        all_res = db_session.query(table_).filter(table_.document[attrib_key].cast(sqlalchemy.String)==attrib_value).order_by(sqlalchemy.desc(table_.updated_on)).limit(result_num).offset(offset)
        return all_res

    def get_all_using_attrib(self, collection, attrib_key, result_num=100, offset=0):
        """ get all aws though attribute value

            arguments:
                collection -- name of the collection (or table), string
                attrib_key --

            returns:
                a list with all the results.
        """
        table_ = getattr(db, collection)
        all_res = db_session.query(table_).order_by(sqlalchemy.desc(table_.updated_on)).order_by(sqlalchemy.desc(table_.updated_on)).limit(result_num).offset(offset)
        return all_res

    def exists(self, collection, identifier):
        """ check if an element already exists in the collection

            arguments:
                collection -- string name of the collection (or table)
                identifier -- string id of the element we want check existance

            return:
                exits -- boolean
        """
        table_ = getattr(db, collection)
        if db_session.query(table_).filter(table_.identifier == identifier).count()>0:
            return True
        else:
            return False
