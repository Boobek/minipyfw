#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ConfigParser, os
from pyqutie import appmeta
cfgname, appcfgdir = appmeta.cfgname, appmeta.appcfgdir

config = ConfigParser.SafeConfigParser()
cpath = os.path.join(appcfgdir, cfgname)
config.read( cpath )


class SavedConfig(object):
    '''
    This class save all attributes immediately to the configuration file (configdir/config.cfg)
    If you want to store something
    '''
    _savedconfigs = {}
    def __new__(cls, configname):
        if configname in SavedConfig._savedconfigs:
            return SavedConfig._savedconfigs[configname]
        else:
            return super(SavedConfig, cls).__new__(cls, configname)


    def __init__(self, configname):
        self._preInt = "**int**"
        self._attributes = {}
        self._configname = configname
        if not config.has_section(configname):
            config.add_section(configname)

        self.__initVariables()
        SavedConfig._savedconfigs[configname] = self


    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        if not name.startswith("_"): #Save it...
            if isinstance(value, int):
                value = self._preInt + str(value)
            config.set(self._configname, name, value)
            self.__writeConf()
            self._attributes[name] = value


    def __initVariables(self):
        sect = self._configname
        for opt in config.options(sect):
            val = config.get(sect, opt)
            if val.startswith(self._preInt):
                val = int(val[len(self._preInt):])
            object.__setattr__(self, opt, val)
            self._attributes[opt] = val


    def getAttributes(self):
        return self._attributes


    def delete(self):
        if config.remove_section(self._configname):
            self.__writeConf()
        else: raise RuntimeError("CONFIG CANNOT DELETED")


    def __writeConf(cls):
        with open(os.path.join(cpath), 'w') as configFile: config.write(configFile)
