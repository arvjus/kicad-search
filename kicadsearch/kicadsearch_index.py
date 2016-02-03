#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import os.path
from whoosh import index
from whoosh.fields import Schema, ID, TEXT, NUMERIC
from whoosh.analysis import StemmingAnalyzer
from .kicadsearch_parser import LibDocCreator, ModDocCreator, KicadModDocCreator


def list_files(rootdirs, sufix):
    for rootdir in rootdirs:
        for root, dirs, files in os.walk(rootdir):
            for path in [root + os.path.sep + file for file in files
                         if file.lower().endswith(sufix)]:
                print(path)
                yield path


class KicadIndexer(object):
    def __init__(self):
        pass

    def create_index(self, indexdir, librarydirs, moduledirs, encoding):
        if not os.path.exists(indexdir):
            os.mkdir(indexdir)

        schema = Schema(id=ID(stored=True),
                        type=TEXT(stored=True),
                        name=TEXT(stored=True),
                        descr=TEXT(stored=True, analyzer=StemmingAnalyzer()),
                        keyword=TEXT(stored=True, analyzer=StemmingAnalyzer()),
                        reference=TEXT(stored=True),
                        md5sum=TEXT(stored=True),
                        path=TEXT(stored=True),
                        position=NUMERIC(stored=True),
                        lineno=NUMERIC(stored=True),
                        lines=NUMERIC(stored=True),
                        path2=TEXT(stored=True),
                        position2=NUMERIC(stored=True),
                        lineno2=NUMERIC(stored=True),
                        lines2=NUMERIC(stored=True), )

        ix = index.create_in(indexdir, schema)
        writer = ix.writer()

        for path in list_files(librarydirs, '.lib'):
            for doc in LibDocCreator(path, encoding).create():
                writer.add_document(**doc)

        for path in list_files(moduledirs, '.mod'):
            for doc in ModDocCreator(path, encoding).create():
                writer.add_document(**doc)

        for path in list_files(moduledirs, '.kicad_mod'):
            for doc in KicadModDocCreator(path, encoding).create():
                writer.add_document(**doc)

        writer.commit()
        searcher = ix.searcher()
        count = searcher.doc_count()
        searcher.close()
        ix.close()
        return count
