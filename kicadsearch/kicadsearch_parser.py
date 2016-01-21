#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, re, hashlib, glob

class ParserException(Exception):
    def __init__(self, msg, path, lineno):
        Exception.__init__(self, 'Error: %s in %s:%d' % (msg, path, lineno))

class LibFileParser(object):
    def __init__(self, path):
        self.path = path
        self.position = 0
        self.lineno = 1
        self.md5sum = None
        self.parsing_item = False
        self.item = {}

    def parse(self):
        if not os.path.isfile(self.path): return None

        with open(self.path, 'r') as f:
            for line in iter(f.readline, ''):
                if line.startswith('DEF'):
                    m = re.match('DEF\s+(\S+)\s.*', line)
                    if not m: raise ParserException('syntax error', self.path, self.lineno)
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
                    self.item['names'] += ' ' + m.group(1).lower()

                elif line.startswith('ENDDEF'):
                    self.item['lines'] += 1
                    self.md5sum.update(line.encode('utf-8'))
                    self.item['md5sum'] = self.md5sum.hexdigest()
                    self.parsing_item = False
                    yield self.item

                self.position = f.tell()
                self.lineno += 1
                if self.parsing_item:
                    self.item['lines'] += 1
                    self.md5sum.update(line.encode('utf-8'))

class DcmFileParser(object):
    def __init__(self, path):
        self.path = path
        self.position = 0
        self.lineno = 1
        self.parsing_item = False
        self.item = {}

    def parse(self):
        if not os.path.isfile(self.path): return None

        with open(self.path, 'r') as f:
            for line in iter(f.readline, ''):
                if line.startswith('$CMP'):
                    m = re.match('\$CMP\s+(\S+)\s+', line)
                    if not m: raise ParserException('syntax error', self.path, self.lineno)
                    self.item = {
                        'name': m.group(1).lower(),
                        'descr': None,
                        'keyword': None,
                        'datasheet': None,
                        'position': self.position,
                        'lineno': self.lineno,
                        'lines': 0,
                        }
                    self.parsing_item = True

                elif line.startswith('D'):
                    m = re.match('^D\s+(.*)$', line)
                    self.item['descr'] = m.group(1).lower()

                elif line.startswith('K'):
                    m = re.match('^K\s+(.*)$', line)
                    self.item['keyword'] = m.group(1).lower()

                elif line.startswith('F'):
                    m = re.match('^F\s+(.*)$', line)
                    self.item['datasheet'] = m.group(1).lower()

                elif line.startswith('$ENDCMP'):
                    self.item['lines'] += 1
                    self.parsing_item = False
                    yield self.item

                self.position = f.tell()
                self.lineno += 1
                if self.parsing_item:
                    self.item['lines'] += 1

class LibDocCreator(object):
    def __init__(self, path):
        self.path = path
        self.path2 = os.path.splitext(path)[0]+'.dcm'
        self.dcm_items = {}
        for item in DcmFileParser(self.path2).parse():
            name = item['name']
            self.dcm_items[name] = item

    def create(self):
        for lib_item in LibFileParser(self.path).parse():
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
                    item['datasheet'] = dcm_item['datasheet']
                    item['path2'] = self.path2
                    item['position2'] = dcm_item['position']
                    item['lineno2'] = dcm_item['lineno']
                    item['lines2'] = dcm_item['lines']
                yield item

if __name__ == '__main__':
    for f in glob.glob(r'./data/library/*.lib'):
        for doc in LibDocCreator(f).create():
            print ('doc:', doc)
