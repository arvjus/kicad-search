#!/usr/bin/python

import os, os.path, glob
from whoosh import index
from whoosh.fields import Schema, ID, TEXT, NUMERIC, STORED
from whoosh.analysis import StemmingAnalyzer
from .kicadsearch_parser import LibDocCreator

class KicadIndexer(object):
    def __init__(self):
        pass

    def create_index(self, indexdir, librarydirs):
        if not os.path.exists(indexdir):
            os.mkdir(indexdir)

        schema = Schema(
            id=ID(stored=True),
            type=TEXT(stored=True),
            name=TEXT(stored=True),
            descr=TEXT(stored=True, analyzer=StemmingAnalyzer()),
            keyword=TEXT(stored=True, analyzer=StemmingAnalyzer()),
            datasheet=TEXT(stored=True),
            md5sum=TEXT(stored=True),
            path=TEXT(stored=True),
            position=NUMERIC(stored=True),
            lineno=NUMERIC(stored=True),
            lines=NUMERIC(stored=True),
            path2=TEXT(stored=True),
            position2=NUMERIC(stored=True),
            lineno2=NUMERIC(stored=True),
            lines2=NUMERIC(stored=True),
            )

        ix = index.create_in(indexdir, schema)
        writer = ix.writer()
        for dir in librarydirs:
            for file in glob.glob(dir):
                print (file)
                for doc in LibDocCreator(file).create():
                    writer.add_document(**doc)
        writer.commit()
        ix.close()
