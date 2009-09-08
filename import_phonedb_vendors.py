#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: expandtab sw=4 ts=4 sts=4:
'''
Wammu website

Tool to import vendors from old phone database.
'''

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import sys
sys.path = ['../'] + sys.path

from phonedb.models import Vendor
import csv

if len(sys.argv) < 2:
    print 'Usage: import_phonedb_vendors.py file.csv'
    sys.exit(1)

input = file(sys.argv[1])
reader = csv.reader(input)
for (id, name, url, slug, tuxmobil) in reader:
    vendor = Vendor()
    vendor.id = int(id)
    vendor.name = name
    vendor.url = url
    vendor.slug = slug
    if tuxmobil != '':
        vendor.tuxmobil = tuxmobil
    print vendor
    vendor.save()
