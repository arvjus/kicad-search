#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from configparser import ConfigParser


class ConfigException(Exception):
    pass


class KicadsrchConfig(ConfigParser):

    def __init__(self, path=None, defaults={}):
        """import properties from config file or provide defaults"""
        ConfigParser.__init__(self, defaults)

        if not path:
            path = os.environ["HOME"] + "/.kicadsearchrc"
        if os.path.exists(path):
            ConfigParser.read(self, path)
        else:
            raise ConfigException('configuration file {} is missing'.format(path))

    def dump_items(self, *sections):
        for sec in [s for s in sections if s in self.sections()]:
            print('section {}:'.format(sec))
            for kv in self.items(sec):
                print('  {} = {}'.format(*kv))
