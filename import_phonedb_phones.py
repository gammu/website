#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: expandtab sw=4 ts=4 sts=4:
'''
Wammu website

Tool to import phones from old phone database.
'''

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import sys
sys.path = ['../'] + sys.path

from phonedb.models import Phone, Connection, Vendor, Feature
import csv
import datetime

if len(sys.argv) < 2:
    print 'Usage: import_phonedb_phones.py file.csv'
    sys.exit(1)

input = file(sys.argv[1])
reader = csv.reader(input)
for (id, vendor, name, features, connection, model, comment, author, email, garble, deleted, created, address, hostname, gammuver) in reader:
    phone = Phone()
    phone.id = int(id)
    phone.vendor = Vendor.objects.get(pk = vendor)
    phone.name = name
    if connection != 'NULL' and connection != '':
        phone.connection = Connection.objects.get(name = connection)
    phone.model = model
    phone.note = unicode(comment, 'utf-8')
    phone.author_name = unicode(author, 'utf-8')
    phone.author_email = unicode(email, 'utf-8')
    phone.email_garble = garble
    if phone.id >= 3038:
        phone.state = 'draft'
    elif deleted == '1':
        phone.state = 'deleted'
    else:
        phone.state = 'approved'
    phone.created = created
    phone.address = address
    phone.hostname = hostname
    phone.gammu_version = gammuver
    phone.save()
    if created != '':
        phone.created = datetime.datetime.strptime(created, '%Y-%m-%d %H:%M:%S')
    # features
    if features != '':
        for feature in features.split(','):
            f = Feature.objects.get(name = feature)
            phone.features.add(f)
    phone.save()
