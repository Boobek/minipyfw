#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import join, exists

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, object_session

# needed for better coding
from sqlalchemy import Column, Integer, Float, String, Date, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship, backref


import logging
from . import appmeta
log = logging.getLogger("pyqutie.database")

# TODO hax for UNICODE TEXTs
from sqlalchemy.interfaces import PoolListener
class SetTextFactory(PoolListener):
    def connect(self, dbapi_con, con_record):
        dbapi_con.text_factory = str


Base = declarative_base()

db_path = join(appmeta.appcfgdir, appmeta.dbname)
db = create_engine('sqlite:///' + db_path, listeners=[SetTextFactory()])
Session = sessionmaker(bind=db)
session = Session()


def store(items):
    # TODO fast hack for object state (if not detached it can't be added)
    for item in items:
        if object_session(item) is None:
            session.add(item)
    log.debug("Items added to the database.")


def save():
    session.commit()
    log.debug("Database saved.")


def first_run():
    log.info("Database path is %s" % db_path)
    print "Database path is %s" % db_path
    metadata = Base.metadata
    metadata.create_all(db)
    save()


if not exists(db_path):
    first_run()
    log.info("Database created")

log.debug("Module loaded")

if __name__ == '__main__':
    first_run()
