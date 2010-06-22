from django.template import RequestContext

from datetime import datetime, timedelta

from django.utils.translation import ugettext as _

import re

BUG_RE = re.compile('(bug ?#([0-9]*))')
LP_RE = re.compile('(LP ?#([0-9]*))')
BDO_RE = re.compile('(bdo ?#([0-9]*))')

class WammuContext(RequestContext):
    def __init__(self, request, context):
        RequestContext.__init__(self, request, context)

def process_bug_links(text):
    '''
    Makes links in form bug #123 clickable to bugs.cihar.com.
    '''
    text = LP_RE.sub(r'[\1](https://bugs.launchpad.net/bugs/\2)', text)
    text = BDO_RE.sub(r'[\1](http://bugs.debian.org/\2)', text)
    return BUG_RE.sub(r'[\1](https://bugs.cihar.com/\2)', text)
