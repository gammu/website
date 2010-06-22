#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: expandtab sw=4 ts=4 sts=4:
'''
Wammu website

Tool to import features from old phone database.
'''

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import sys
sys.path = ['../'] + sys.path

from phonedb.models import Feature

if len(sys.argv) < 2:
    print 'Usage: import_phonedb_features.py feature,feature,...'
    sys.exit(1)

for text in sys.argv[1].split(','):
    feature = Feature()
    feature.name = text
    print feature
    feature.save()
