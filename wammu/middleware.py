from django.contrib.sites.models import Site
from django.utils import translation


class SiteLocaleMiddleware(object):
    def process_request(self, request):
        current_site = Site.objects.get_current()

        lang = current_site.domain.split('.')[0]
        if len(lang) == 2:
            translation.activate(lang)
            request.LANGUAGE_CODE = translation.get_language()
