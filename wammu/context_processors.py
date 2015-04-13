# Context processors
# -*- coding: UTF-8 -*-

from django.conf import settings
from datetime import datetime
from django.utils.translation import ugettext as _, get_language

def translations(request):
    path = request.get_full_path()
    langs = []

    lang = get_language()

    if lang != 'cs':
        langs.append({'url': 'http://cs.wammu.eu%s' % path, 'name': u'Česky', 'code': 'cs-CZ'})

    if lang != 'en':
        langs.append({'url': 'http://wammu.eu%s' % path, 'name': u'English', 'code': 'en-US'})

    if lang != 'es':
        langs.append({'url': 'http://es.wammu.eu%s' % path, 'name': u'Español', 'code': 'es-ES'})

    if lang != 'de':
        langs.append({'url': 'http://de.wammu.eu%s' % path, 'name': u'Deutsch', 'code': 'de-DE'})

    if lang != 'sk':
        langs.append({'url': 'http://sk.wammu.eu%s' % path, 'name': u'Slovenčina', 'code': 'sk-SK'})

    if lang != 'fr':
        langs.append({'url': 'http://fr.wammu.eu%s' % path, 'name': u'Français', 'code': 'fr-FR'})

    if lang != 'pt-br':
        langs.append({'url': 'http://pt-br.wammu.eu%s' % path, 'name': u'Português brasileiro', 'code': 'pt-BR'})

    return {'translations': langs}

def message(request):
    ret = {}
    if request.session.has_key('message'):
        ret['message'] = request.session['message']
        del request.session['message']
    return ret

def dates(request):
    return {
        'current_year': datetime.now().strftime('%Y'),
        'generated': datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT'),
    }

def feeds(request):
    return {'global_feeds': [
            {'url': '/news/rss/', 'title': _('Gammu and Wammu News Feed (RSS)'), 'type': 'application/rss+xml'},
            {'url': '/news/atom/', 'title': _('Gammu and Wammu News Feed (Atom)'), 'type': 'application/atom+xml'},
    ]}
