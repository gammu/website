from django.contrib.sites.models import get_current_site
from django.utils import translation


class SiteLocaleMiddleware(object):
    def process_request(self, request):
        current_site = get_current_site(request)

        lang = current_site.domain.split('.')[0]
        if len(lang) == 2:
            translation.activate(lang)
            request.LANGUAGE_CODE = translation.get_language()
        else:
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
