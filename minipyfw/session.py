#!/usr/bin/env python
# -*- coding: utf-8 -*-
from AppMeta import configdir
import os
import datetime
import logging
log = logging.getLogger("pyqutie.session")

__session = None
class Session(object):
    def __new__(cls):
        if not __session:
            sess = object.__new__(cls)
            global __session
            __session = sess
            return __session
        else: return __session


    def __init__(self):
        self.reset()

    def reset(self):
        self.date = datetime.datetime.now()
        self.id = -1
        self.state = -1                 # Current activitys unique id
        self.process = 0                # process of the activity. This value can be used
                                        #  when finished or skipped the learning and watching
                                        #  or reading video/webarticle. This value contain
                                        #  the saved second in the video or percent of the
                                        #  arcticle
        self.loaded = False             # Session is loaded?
        log.info("New session created")


    def loadSession(self, session):
        self.date = session.date
        self.id = session.id
        self.state = session.state
        self.process = session.process
        self.loaded = True
        log.info("Session loaded")


    def isLoaded(self):
        return self.loaded


    def text(self):
        return "%(state)s\n    at %(date)s" % \
                {"state": self.stateText(), "date": self.date.strftime("%m/%d %H:%M")}


    def stateText(self):
        from pluginloader import plugins
        return plugins[self.state].meta.visiblename


_sessionfilepath = os.path.join(configdir, "sessions.bak")
def saveSession(sess):
    sessions = listSessions()

    if sess.id == -1:
        maxid = -1
        for id in sessions:
            if id > maxid:
                maxid = id
        sess.id = maxid + 1
    sess.date = datetime.datetime.now()

    sessions[sess.id] = sess
    __saveSessions(sessions)


def __saveSessions(sessions):
    import cPickle as pickle
    f = open(_sessionfilepath, 'w')
    pickle.dump(sessions, f)
    f.close()
    log.info("Sessions saved to %s.", _sessionfilepath)


def removeSession(sess_id):
    sessions = listSessions()
    del sessions[sess_id]
    __saveSessions(sessions)
    log.info("Session removed. (id: %s)", sess_id)


def loadSession(sess_id):
    loaded = listSessions()[sess_id]
    Session().loadSession(loaded)
    log.info("Session loaded. (id: %s)", sess_id)


def listSessions():
    import cPickle as pickle
    if not os.path.exists(_sessionfilepath):
        return {}

    f = open(_sessionfilepath, 'r')
    sessions = pickle.load(f)
    f.close()

    ret = {}
    for s in sessions:
        ret[s] = sessions[s]
    return ret
