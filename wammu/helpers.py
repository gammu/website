from django.template import RequestContext

from datetime import datetime, timedelta

class WammuContext(RequestContext):
    def __init__(self, request, context):
        context['current_year'] = datetime.now().strftime('%Y')
        context['generated'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
        context['menu'] = [{'title': 'Gammu', 'link': '/gammu/'}]
        RequestContext.__init__(self, request, context)

