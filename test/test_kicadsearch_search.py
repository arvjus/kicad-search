#!/usr/bin/python
# -*- coding: utf-8 -*-

from kicadsearch import KicadSearcher


def test_KicadSearcher():
    ks = KicadSearcher('./test/data/index')
    ks.search('4n*', None, None, None, False)
