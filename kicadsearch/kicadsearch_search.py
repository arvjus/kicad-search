#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from whoosh import index
from whoosh.query import Every
from whoosh.qparser import QueryParser, MultifieldParser, FieldAliasPlugin, OrGroup


class KicadSearcher(object):

    def __init__(self, indexdir):
        self.indexdir = indexdir
        self.ix = index.open_dir(self.indexdir)
        self.searcher = self.ix.searcher()

    def close(self):
        self.searcher.close()

    def print_index_statistics(self):
        print('location:   ', self.indexdir)
        print('num of docs:', self.searcher.doc_count())
        print('terms:       id, type,  name, descr, keyword, reference, md5sum')
        print('terms:       path, position, lineno, lines')
        print('terms:       path2, position2, lineno2, lines2')
        print()

    def search(self, query, limit, any_match, search_type, print_docs):
        if any_match:
            parser = MultifieldParser(
                ['name', 'keyword', 'descr'], self.ix.schema, group=OrGroup)
        else:
            parser = QueryParser('name', self.ix.schema)
        parser.add_plugin(FieldAliasPlugin({'type': 't',
                                            'name': 'n',
                                            'keyword': 'k',
                                            'descr': 'd'}))
        print_hit = self.print_doc if print_docs else self.print_meta
        query = parser.parse(query)
        if search_type:
            query = parser.parse('type:{}'.format(search_type)) & query
        for hit in self.searcher.search(query, limit=limit):
            print_hit(hit)

    def list_all(self, print_docs):
        print_hit = self.print_doc if print_docs else self.print_meta
        for hit in self.searcher.search(Every(), limit=sys.maxsize):
            print_hit(hit)

    def print_meta(self, doc):
        keys = doc.keys()
        print('type:      {}'.format(doc['type']))
        print('name:      {}'.format(doc['name']))
        if 'descr' in keys:
            print('descr:     {}'.format(doc['descr']))
        if 'keyword' in keys:
            print('keyword:   {}'.format(doc['keyword']))
        if 'reference' in keys:
            print('reference: {}'.format(doc['reference']))
        print('location:  {}:{}-{}'.format(doc['path'], doc['lineno'], doc[
            'lineno'] + doc['lines'] - 1))
        if 'path2' in keys:
            print('location:  {}:{}-{}'.format(doc['path2'], doc[
                'lineno2'], doc['lineno2'] + doc['lines2'] - 1))
        print('md5sum:    {}'.format(doc['md5sum']))
        print()

    def print_doc(self, doc):
        def dump_doc(path, position, lines):
            try:
                with open(path, 'r') as f:
                    f.seek(position)
                    for n in range(lines):
                        print(f.readline(), end="", flush=True)
            except FileNotFoundError:
                print('reading error or file {} is no longer available'.format(path))
            finally:
                print()

        dump_doc(doc['path'], doc['position'], doc['lines'])
        if 'path2' in doc.keys():
            dump_doc(doc['path2'], doc['position2'], doc['lines2'])
