from django.contrib.sites.models import Site
from django.utils import translation


class SiteLocaleMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        self.process_request(request)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_request(self, request):
        try:
            current_site = Site.objects.get_current(request)

            lang = current_site.domain.split('.')[0]
            if lang == 'wammu':
                translation.activate('en')
            elif len(lang) == 2 or len(lang) == 5:
                translation.activate(lang)
                request.LANGUAGE_CODE = translation.get_language()
            else:
                translation.activate('en')
        except Site.DoesNotExist:
            translation.activate('en')
