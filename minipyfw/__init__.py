#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
def __setLogging():
    import logging
    #filename = 'execution.log'
    #filemode = 'w'
    level = logging.DEBUG
    datefmt = '%m/%d %H:%M:%S'
    format = '%(asctime)s [%(levelname)s %(name)s] %(message)s'
    #if level == logging.DEBUG:
    #    format += '\n\t%(pathname)s:%(lineno)d\n'

    #logging.basicConfig(filename=filename, filemode=filemode, format=format, datefmt=datefmt, level=level)
    logging.basicConfig(format=format, datefmt=datefmt, level=level)


def __parseOptions(args=sys.argv):
    import argparse
    parser = argparse.ArgumentParser(description='`%s\' launcher and debugger' % appmeta.name)
    parser.add_argument('-d', '-debug', dest='debug', action='store_true',
                       help='debug mode')
    parser.add_argument('-c', '-creator', dest='creator', action='store_true',
                       help='creator mode')
    parser.add_argument('-s', '-start', dest='start', action='store_true',
                       help='start application')
    return parser.parse_args(args)


def runApp():
    ''' Run Gui Application. Invoke this method in production mode. '''
    from PySide.QtGui import QApplication, QSplashScreen, QPixmap
    #from appmeta import resdir, name

    app = QApplication([])
    app.setApplicationName(appmeta.name)

    splash = QSplashScreen( QPixmap(join(appmeta.resdir, "pixmaps", "splash-small.png")) )
    splash.show()

    from pyqutie.plugins import loadPlugins
    loadPlugins()

    from pyqutie.gui.window import getWindow
    splash.finish( getWindow() )

    app.exec_()


def runCmd(args):
    ''' Run Gui Application with commandline parsing. Invoke this method in development mode. '''
    __setLogging()
    args = __parseOptions(args)
    print "parsing"
    if args.debug:
        from pyqutie import debug
        debug.run()
    elif args.creator:
        import pyqutiecreator as creator
        creator.run()
    elif args.start:
        runApp()


import locale, logging, os, platform
from os.path import join, exists
from os import environ as envs

log = logging.getLogger("pyqutie.appmeta")

class __AppMeta(object):
    ''' This class contain the application's meta attributes.
    You must set application's basepath firstli
    '''
    def __init__(self):
        #############################
        # Application specific things
        self.url = "www.bkanyo.com"
        self.name = "Application created by pqutie(%s)" % self.url
        self.shortname = "pyqutie"
        self.motto = "appmotto"
        self.desc = '''appdesc'''
        self.ver = "1.0"
        self.devs = "Balazs KANYO, email: bkanyo@gmail.com"

        self.dbname = "base.db"
        self.cfgname = "config.cfg"

        self.__appBaseVar = None
        self.encoding = locale.getpreferredencoding()


    def setupApplication(self, name, shortname, motto="Motto", desc="Description", version="1.0", developers=None, url="http://example.com"):
        self.name = name
        shel.shortname = shortname
        self.motto = motto
        self.desc = desc
        self.version = version
        if developers is not None:
            self.developers = developers
        else:
            self.developers = self.name + " developers"
        self.url = url

    @property
    def appBase(self):
        if self.__appBaseVar == None:
            raise RuntimeError("Firstly set the application's path like this: appmeta.appBase = __file__")
        return self.__appBaseVar

    @appBase.setter
    def appBase(self, path):
        ''' Set application base directory '''
        if os.path.isfile(path):
            path = os.path.dirname(path)
        self.__appBaseVar = path
        self._createDirs()


    @property
    def appcfgdir(self):
        ''' configuration directory '''
        if "pyqutie-debug" in envs and envs["pyqutie-debug"] == "True":
            return join(self.appBase, "config_dir")
        elif platform.system() == "Linux":
            return join(envs['XDG_DATA_HOME'], self.shortname)
        else:
            raise NotImplementedError()


    @property
    def resdir(self):
        ''' resources directory '''
        return join(self.appBase, "resources")


    def _createDirs(self):
        print self.appcfgdir
        if not exists(self.appcfgdir):
            os.makedirs(self.appcfgdir)
            log.info("Configuration directory created: %s", self.appcfgdir)
appmeta = __AppMeta()