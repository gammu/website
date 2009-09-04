#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: expandtab sw=4 ts=4 sts=4:
'''
Wammu website

Takes a HTMLized man page and process it to something includable in pages.
'''

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import sys
sys.path = ['../'] + sys.path

from xml.dom import minidom


dom = minidom.parse(sys.argv[1])
body = dom.getElementsByTagName('body')[0]
# Drop body element and use <div class="manpage"> instead
body.tagName = 'div'
body.setAttribute('class', 'manpage')
# Lower headings (eg. h1 becomes h2)
for idx in xrange(7, 0, -1):
    for el in body.getElementsByTagName('h%d' % idx):
        el.tagName = 'h%d' % (idx + 1)
# Fixup links
for el in body.getElementsByTagName('a'):
    href = el.getAttribute('href')
    # Links without target need a class not to be marked as links
    if href == '':
        el.setAttribute('class', 'aname')
    # We don't need index links
    elif href == '../index.html':
        el.parentNode.removeChild(el)
    # Fix links to other pages
    elif href[-5:] == '.html' and href.find('://') == -1:
        el.setAttribute('href', '../%s/' % href[:-5])
# Output xml
print body.toxml(encoding = 'utf-8')

