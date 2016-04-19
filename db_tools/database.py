"""
database.py

a simple configuration and init for the postgresql db

:copyright: (c) 2016 Internet Archive.
:   author: Giovanni Damiola <gio@archive.org>
"""


from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import config

engine = create_engine(config.PSQL_URI, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models
    import db_model
    Base.metadata.create_all(bind=engine)
