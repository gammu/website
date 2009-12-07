# Context processors
# -*- coding: UTF-8 -*-

from django.conf import settings

def translations(request):
    path = request.get_full_path()
    langs = []

    if settings.LANGUAGE_CODE != 'cs-cz':
        langs.append({'url': 'http://cs.wammu.eu%s' % path, 'name': u'Česky'})

    if settings.LANGUAGE_CODE != 'en-us':
        langs.append({'url': 'http://wammu.eu%s' % path, 'name': u'English'})

    if settings.LANGUAGE_CODE != 'es-es':
        langs.append({'url': 'http://es.wammu.eu%s' % path, 'name': u'Español'})

    return {'translations': langs}
