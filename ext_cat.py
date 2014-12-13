# -*- coding: utf-8 -*-
#!/usr/bin/python

import sys

if len(sys.argv) < 2:
    print 'Usage ext_cat.py file_name1, ... file_nameN'
    raise SystemExit(1)

del sys.argv[0]

for file_name in sys.argv:
    try:
        with open(file_name, 'r') as file:
            for line in file:
                print line
    except IOError as e:
        print u'IOError error({0}): {1} filename={2}'.format(e.errno, e.strerror, e.filename)