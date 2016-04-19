"""
db_model.py

a basic database model for rapni.py

:copyright: (c) 2016 Internet Archive.
:   author: Giovanni Damiola <gio@archive.org>
"""

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import JSON, JSONB
from sqlalchemy.orm import relationship
from database import Base

import datetime


class JsonTable(Base):
    __abstract__ = True
    identifier = Column(String(100), primary_key=True)
    document = Column(JSON, nullable=False)
    created_on = Column(DateTime, default=datetime.datetime.utcnow)
    updated_on = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


    def __init__(self, identifier=None, document=None):
        self.identifier = identifier
        self.document = document

    def __repr__(self):
        return '<%r>' % (self.identifier)


class Documents(JsonTable):
    __tablename__ = 'documents'



class Events(JsonTable):
    __tablename__ = 'iabevents'
    identifier = Column(Integer, primary_key=True, autoincrement=True)

    def __init__(self, document=None):
        self.document = document
