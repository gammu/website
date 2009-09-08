#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: expandtab sw=4 ts=4 sts=4:
'''
Wammu website

Tool to import connections from old phone database.
'''

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import sys
sys.path = ['../'] + sys.path

from phonedb.models import Connection
import csv

if len(sys.argv) < 2:
    print 'Usage: import_phonedb_connections.py connection,connection,...'
    sys.exit(1)

for text in sys.argv[1].split(','):
    connection = Connection()
    connection.name = text
    if text.find('irda') != -1:
        connection.medium = 'irda'
    elif text.find('blue') != -1:
        connection.medium = 'bluetooth'
    elif text.find('usb') != -1:
        connection.medium = 'usb'
    elif text.find('dku') != -1:
        connection.medium = 'usb'
    elif text.find('dlr') != -1:
        connection.medium = 'usb'
    elif text.find('pl2303') != -1:
        connection.medium = 'usb'
    else:
        connection.medium = 'serial'
    print connection
    connection.save()

