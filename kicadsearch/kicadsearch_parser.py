#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import hashlib


class ParserException(Exception):

    def __init__(self, msg, path, lineno):
        Exception.__init__(self, 'Error: %s in %s:%d' % (msg, path, lineno))


###############################################################################
# Symbol library
###############################################################################
class LibFileParser(object):

    def __init__(self, path, encoding):
        self.path = path
        self.encoding = encoding
        self.position = 0
        self.lineno = 1
        self.md5sum = None
        self.parsing_item = False
        self.item = {}

    def parse(self):
        if not os.path.isfile(self.path):
            return None

        with open(self.path, 'r', encoding=self.encoding) as f:
            try:
                for line in iter(f.readline, ''):
                    if line.startswith('DEF'):
                        m = re.match('DEF\s+(\S+)\s.*', line)
                        if not m:
                            raise ParserException(
                                'syntax error', self.path, self.lineno)
                        self.item = {
                            'names': m.group(1).lower(),
                            'position': self.position,
                            'lineno': self.lineno,
                            'lines': 0,
                        }
                        self.md5sum = hashlib.md5()
                        self.parsing_item = True

                    elif line.startswith('ALIAS'):
                        m = re.match('^ALIAS\s+(.*)$', line)
                        if m:
                            self.item['names'] += ' ' + m.group(1).lower()

                    elif line.startswith('ENDDEF'):
                        self.item['lines'] += 1
                        self.md5sum.update(line.encode(self.encoding))
                        self.item['md5sum'] = self.md5sum.hexdigest()
                        self.parsing_item = False
                        yield self.item

                    self.position = f.tell()
                    self.lineno += 1
                    if self.parsing_item:
                        self.item['lines'] += 1
                        self.md5sum.update(line.encode(self.encoding))
            except Exception as ex:
                print('Error:', ex)


class DcmFileParser(object):

    def __init__(self, path, encoding):
        self.path = path
        self.encoding = encoding
        self.position = 0
        self.lineno = 1
        self.parsing_item = False
        self.item = {}

    def parse(self):
        if not os.path.isfile(self.path):
            return None

        with open(self.path, 'r', encoding=self.encoding) as f:
            try:
                for line in iter(f.readline, ''):
                    if line.startswith('$CMP'):
                        m = re.match('\$CMP\s+(\S+)\s+', line)
                        if not m:
                            raise ParserException(
                                'syntax error', self.path, self.lineno)
                        self.item = {
                            'name': m.group(1).lower(),
                            'descr': None,
                            'keyword': None,
                            'reference': None,
                            'position': self.position,
                            'lineno': self.lineno,
                            'lines': 0,
                        }
                        self.parsing_item = True

                    elif line.startswith('D'):
                        m = re.match('^D\s+(.*)$', line)
                        if m:
                            self.item['descr'] = m.group(1).lower()

                    elif line.startswith('K'):
                        m = re.match('^K\s+(.*)$', line)
                        if m:
                            self.item['keyword'] = m.group(1).lower()

                    elif line.startswith('F'):
                        m = re.match('^F\s+(.*)$', line)
                        if m:
                            self.item['reference'] = m.group(1).lower()

                    elif line.startswith('$ENDCMP'):
                        self.item['lines'] += 1
                        self.parsing_item = False
                        yield self.item

                    self.position = f.tell()
                    self.lineno += 1
                    if self.parsing_item:
                        self.item['lines'] += 1
            except Exception as ex:
                print('Error:', ex)


class LibDocCreator(object):

    def __init__(self, path, encoding):
        self.path = path
        self.encoding = encoding
        self.path2 = os.path.splitext(path)[0] + '.dcm'
        self.dcm_items = {}
        for item in DcmFileParser(self.path2, self.encoding).parse():
            name = item['name']
            self.dcm_items[name] = item

    def create(self):
        for lib_item in LibFileParser(self.path, self.encoding).parse():
            for name in lib_item['names'].split():
                item = lib_item.copy()
                item['id'] = '{}#{}'.format(self.path, name)
                item['type'] = 'LIB'
                item['path'] = self.path
                item['name'] = name
                del item['names']
                if name in self.dcm_items.keys():
                    dcm_item = self.dcm_items[name]
                    item['descr'] = dcm_item['descr']
                    item['keyword'] = dcm_item['keyword']
                    item['reference'] = dcm_item['reference']
                    item['path2'] = self.path2
                    item['position2'] = dcm_item['position']
                    item['lineno2'] = dcm_item['lineno']
                    item['lines2'] = dcm_item['lines']
                yield item


###############################################################################
# Footprint library .mod
###############################################################################
class ModFileParser(object):

    def __init__(self, path, encoding):
        self.path = path
        self.encoding = encoding
        self.position = 0
        self.lineno = 1
        self.md5sum = None
        self.parsing_item = False
        self.item = {}

    def parse(self):
        if not os.path.isfile(self.path):
            return None

        with open(self.path, 'r', encoding=self.encoding) as f:
            try:
                for line in iter(f.readline, ''):
                    if line.startswith('$MODULE'):
                        m = re.match('\$MODULE\s+(\S+)\s.*', line)
                        if not m:
                            raise ParserException(
                                'syntax error', self.path, self.lineno)
                        self.item = {
                            'names': m.group(1).lower(),
                            'position': self.position,
                            'lineno': self.lineno,
                            'lines': 0,
                        }
                        self.md5sum = hashlib.md5()
                        self.parsing_item = True

                    elif line.startswith('Cd'):
                        m = re.match('^Cd\s+(.*)$', line)
                        if m:
                            self.item['descr'] = m.group(1).lower()

                    elif line.startswith('K'):
                        m = re.match('^Kw\s+(.*)$', line)
                        if m:
                            self.item['keyword'] = m.group(1).lower()

                    elif line.startswith('AR'):
                        m = re.match('^AR\s+(.*)$', line)
                        if m:
                            self.item['reference'] = m.group(1).lower()

                    elif line.startswith('$EndMODULE'):
                        self.item['lines'] += 1
                        self.md5sum.update(line.encode(self.encoding))
                        self.item['md5sum'] = self.md5sum.hexdigest()
                        self.parsing_item = False
                        yield self.item

                    self.position = f.tell()
                    self.lineno += 1
                    if self.parsing_item:
                        self.item['lines'] += 1
                        self.md5sum.update(line.encode(self.encoding))
            except Exception as ex:
                print('Error:', ex)


class ModDocCreator(object):

    def __init__(self, path, encoding):
        self.path = path
        self.encoding = encoding

    def create(self):
        for lib_item in ModFileParser(self.path, self.encoding).parse():
            for name in lib_item['names'].split():
                item = lib_item.copy()
                item['id'] = '{}#{}'.format(self.path, name)
                item['type'] = 'MOD'
                item['path'] = self.path
                item['name'] = name
                del item['names']
                yield item


###############################################################################
# Footprint library .kicad_mod
###############################################################################
class KicadModFileParser(object):

    def __init__(self, path, encoding):
        self.path = path
        self.encoding = encoding
        self.md5sum = None
        self.item = {}

    def parse(self):
        if not os.path.isfile(self.path):
            return None

        with open(self.path, 'r', encoding=self.encoding) as f:
            try:
                for line in iter(f.readline, ''):
                    while True:
                        m = re.search('\(module\s+(\S+).*', line)
                        if m:
                            self.item = {
                                'name': m.group(1).lower(),
                                'position': 0,
                                'lineno': 1,
                                'lines': 0,
                            }
                            self.md5sum = hashlib.md5()
                            break

                        m = re.search('\(descr\s+"*([^"\)]+)"*\)', line)
                        if m:
                            self.item['descr'] = m.group(1).lower()
                            break

                        m = re.search('\(tags\s+"*([^"\)]+)"*\)', line)
                        if m:
                            self.item['keyword'] = m.group(1).lower()
                        break
                    self.item['lines'] += 1
                    self.md5sum.update(line.encode(self.encoding))

                self.item['md5sum'] = self.md5sum.hexdigest()
                yield self.item
            except Exception as ex:
                print('Error:', ex)


class KicadModDocCreator(object):

    def __init__(self, path, encoding):
        self.path = path
        self.encoding = encoding

    def create(self):
        for lib_item in KicadModFileParser(self.path, self.encoding).parse():
            item = lib_item.copy()
            item['id'] = '{}#{}'.format(self.path, item['name'])
            item['type'] = 'KMOD'
            item['path'] = self.path
            yield item
