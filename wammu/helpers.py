from django.template import RequestContext

from datetime import datetime, timedelta

from django.utils.translation import ugettext as _

import re

BUG_RE = re.compile('(bug ?#([0-9]*))')
LP_RE = re.compile('(LP ?#([0-9]*))')

class WammuContext(RequestContext):
    def __init__(self, request, context):
        context['current_year'] = datetime.now().strftime('%Y')
        context['generated'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
        context['menu'] = [
            {'title': _('Support'), 'link': '/support/'},
            {'title': _('Download'), 'link': '/download/'},
            {'title': _('Screenshots'), 'link': '/screenshots/'},
            {'title': _('Documentation'), 'link': '/docs/'},
            {'title': _('Contribute'), 'link': '/contribute/'},
            ]
        if not context.has_key('feeds'):
            context['feeds'] = []
        context['feeds'].append(
            {'url': '/news/rss/', 'title': _('Gammu and Wammu News Feed (RSS)'), 'type': 'application/rss+xml'}
            )
        context['feeds'].append(
            {'url': '/news/atom/', 'title': _('Gammu and Wammu News Feed (Atom)'), 'type': 'application/atom+xml'}
            )
        if request.session.has_key('message'):
            context['message'] = request.session['message']
            del request.session['message']
        RequestContext.__init__(self, request, context)

def process_bug_links(text):
    '''
    Makes links in form bug #123 clickable to bugs.cihar.com.
    '''
    text = LP_RE(sub(r'[\1](https://bugs.launchpad.net/bugs/\2)', text)
    return BUG_RE.sub(r'[\1](https://bugs.cihar.com/\2)', text)
