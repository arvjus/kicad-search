#!/usr/bin/python
# -*- coding: utf-8 -*-

import pytest
from kicadsearch import KicadsrchConfig
from configparser import NoOptionError

def test_default_KicadsrchConfig():
    config = KicadsrchConfig('kicadsearchrc.sample')
    assert config.get('default', 'indexdir') == './test/data/index'
    assert config.get('index', 'encoding') == 'latin1'

def test_nonexist_KicadsrchConfig():
    config = KicadsrchConfig('kicadsearchrc.sample')
    with pytest.raises(NoOptionError):
        config.get('search', 'non-existing')
