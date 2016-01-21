#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from configparser import ConfigParser, NoSectionError

class ConfigException(Exception):
    pass

class KicadsrchConfig(ConfigParser):
    def __init__(self, path = None):
        """import properties from config file or provide defaults"""
        ConfigParser.__init__(self)

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

if __name__ == '__main__':
    config = KicadsrchConfig(None)
    config.dump_items('default', 'index', 'search')