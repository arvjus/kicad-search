#!/usr/bin/python
# -*- coding: utf-8 -*-

import glob
from kicadsearch import LibFileParser, DcmFileParser, LibDocCreator
from kicadsearch import ModFileParser, ModDocCreator
from kicadsearch import KicadModFileParser, KicadModDocCreator

# .lib, .dcm
def test_LibFileParser():
    docs = []
    for f in glob.glob(r'./test/data/library/*.lib'):
        docs += [doc for doc in LibFileParser(f, 'latin1').parse()]
    assert len(docs) == 54

def test_DcmFileParser():
    docs = []
    for f in glob.glob(r'./test/data/library/*.dcm'):
        docs += [doc for doc in DcmFileParser(f, 'latin1').parse()]
    assert len(docs) == 71

def test_LibDocCreator():
    docs = []
    for f in glob.glob(r'./test/data/library/*.lib'):
        docs += [doc for doc in LibDocCreator(f, 'latin1').create()]
    assert len(docs) == 86

# .mod
def test_ModFileParser():
    docs = []
    for f in glob.glob(r'./test/data/library/*.mod'):
        docs += [doc for doc in ModFileParser(f, 'latin1').parse()]
    assert len(docs) == 9

def test_ModDocCreator():
    docs = []
    for f in glob.glob(r'./test/data/library/*.mod'):
        docs += [doc for doc in ModDocCreator(f, 'latin1').create()]
    assert len(docs) == 9

# .kicad_mod
def test_KicadModFileParser():
    docs = []
    for f in glob.glob(r'./test/data/library/*.pretty/*.kicad_mod'):
        docs += [doc for doc in KicadModFileParser(f, 'latin1').parse()]
    assert len(docs) == 1

def test_KicadModDocCreator():
    docs = []
    for f in glob.glob(r'./test/data/library/*.pretty/*.kicad_mod'):
        docs += [doc for doc in KicadModDocCreator(f, 'latin1').create()]
    assert len(docs) == 1
