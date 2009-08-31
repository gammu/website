from django.template import RequestContext

from datetime import datetime, timedelta

from django.utils.translation import ugettext as _

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
        context['feeds'] = [
            {'url': '/news/rss/', 'title': _('Gammu and Wammu News Feed (RSS)'), 'type': 'application/rss+xml'},
            {'url': '/news/atom/', 'title': _('Gammu and Wammu News Feed (Atom)'), 'type': 'application/atom+xml'},
        ]
        RequestContext.__init__(self, request, context)

