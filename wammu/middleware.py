from django.contrib.sites.models import get_current_site
from django.utils import translation


class SiteLocaleMiddleware(object):
    def process_request(self, request):
        current_site = get_current_site()

        lang = current_site.domain.split('.')[0]
        if len(lang) == 2:
            translation.activate(lang)
            request.LANGUAGE_CODE = translation.get_language()
