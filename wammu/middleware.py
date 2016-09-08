from django.contrib.sites.models import Site
from django.utils import translation


class SiteLocaleMiddleware(object):
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


class HTTPHeadersMiddleware(object):
    """
    Middleware that sets the Strict-Transport-Security HTTP header in HTTP
    responses.

    Does not set the header if it's already set.
    """
    def process_response(self, request, response):
        # Don't set it if it's already in the response
        if response.get('X-Frame-Options', None) is None:
            response['X-Frame-Options'] = 'DENY'

        return response
