from django.template import RequestContext

from datetime import datetime, timedelta

from django.utils.translation import ugettext as _

import re

BUG_RE = re.compile('(bug ?#([0-9]*))')

class WammuContext(RequestContext):
    def __init__(self, request, context):
        context['current_year'] = datetime.now().strftime('%Y')
        context['generated'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
        context['menu'] = [
            {'title': 'Support', 'link': '/support/'},
            {'title': 'Download', 'link': '/download/'},
            {'title': 'Screenshots', 'link': '/screenshots/'},
            {'title': 'Documentation', 'link': '/docs/'},
            {'title': 'Contribute', 'link': '/contribute/'},
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
    return BUG_RE.sub(r'[\1](https://bugs.cihar.com/\2)', text)
