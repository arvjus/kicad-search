#!/usr/bin/python
# -*- coding: utf-8 -*-

from kicadsearch import KicadIndexer


def test_KicadIndexer():
    ki = KicadIndexer()
    count = ki.create_index('./test/data/index', ['./test/data/library'],
                            ['./test/data/library'], 'latin1')
    assert count == 96
