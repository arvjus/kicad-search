
KiCad Search
========

Freetext searching in KiCad EDA component libraries

Copyright (c) 2016 Arvid Juskaitis

features:

 - support for schematic part library (*.lib, *.dcm)
 - support for module libraries (*.kicad_mod) and 'legacy' format (*.mod)
 - flexible search queries
 - powered by whoosh
 - cli interface


Quick Start
--------------

After downloading, un-tar archive, cd to package root:

> $ tar xzf KicadSearch-x.x.x.tar.gz

> $ cd KicadSearch-x.x.x

Install python modules and scripts:

> $ sudo python setup.py install

Create configuration:

> $ cp kicadsearchrc.sample ~/.kicadsearchrc

Edit ~/.kicadsearchrc - setup variables according your environment

Check configuration:

> $ kicadsearch-index -C

Index libraries:

> $ kicadsearch-index -I

Print index info:

> $ kicadsearch -P


Searching
------------

These fields contain searchable information of components: *type*, *name*, *keyword*, *descr*. *name* field is default, i.e you don't need to type explicitly for simple queries.
It is sufficient to type the first letter for the field, like *k:* or *d:* in a query.

Search by name with wildcard:

> $ kicadsearch '74*'

Search by name on any of two components:

> $ kicadsearch '74ls688 OR 74ls689'

Search any of two components in any of field:

> $ kicadsearch -a '74ls688 74ls689'

Search only within a given type:

> $ kicadsearch -t lib -a '74ls688 74ls689'

Search by name and keyword:

> $ kicadsearch 'n:zener* AND k:diode'

Slightly more advanced search:

> $ kicadsearch 'k:arm AND (d:i2c OR d:spi)'

Dump content of library component:

> $ kicadsearch '74ls688' -d

List all documents:

> $ kicadsearch -L

