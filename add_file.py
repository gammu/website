#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: expandtab sw=4 ts=4 sts=4:
'''
Wammu website

Takes a filename and inserts it into downloads database.
'''

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import sys
sys.path = ['../'] + sys.path

import hashlib

from downloads.models import Release, Download

if len(sys.argv) < 5:
    print 'Usage: add_file.py /base/path program version file...'
    print '       file can containt type as file:type, eg. setup-1.2.3.exe:win32'
    sys.exit(1)

release = Release.objects.get(program = sys.argv[2], version = sys.argv[3])

dlpath = sys.argv[1]

while dlpath[-1] == '/':
    dlpath = dlpath[:-1]

for f in sys.argv[4:]:
    print "Adding %s..." % f
    path, filename_type = os.path.split(f)
    try:
        filename, type = filename_type.split(':')
    except ValueError:
        filename = filename_type
        type = 'source'

    data = open(f).read()

    dl = Download()
    dl.release = release

    md5 = hashlib.md5()
    md5.update(data)
    dl.md5 = md5.hexdigest()

    sha1 = hashlib.sha1()
    sha1.update(data)
    dl.sha1 = sha1.hexdigest()

    dl.size = len(data)

    dl.platform = type

    dl.location = '%s/%s' % (dlpath, filename)

    dl.save()
