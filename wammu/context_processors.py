# Context processors
# -*- coding: UTF-8 -*-

from django.conf import settings
from datetime import datetime
from django.utils.translation import ugettext as _

def translations(request):
    path = request.get_full_path()
    langs = []

    if settings.LANGUAGE_CODE != 'cs-cz':
        langs.append({'url': 'http://cs.wammu.eu%s' % path, 'name': u'Česky'})

    if settings.LANGUAGE_CODE != 'en-us':
        langs.append({'url': 'http://wammu.eu%s' % path, 'name': u'English'})

    if settings.LANGUAGE_CODE != 'es-es':
        langs.append({'url': 'http://es.wammu.eu%s' % path, 'name': u'Español'})

    if settings.LANGUAGE_CODE != 'de-de':
        langs.append({'url': 'http://de.wammu.eu%s' % path, 'name': u'Deutsch'})

    if settings.LANGUAGE_CODE != 'sk-sk':
        langs.append({'url': 'http://sk.wammu.eu%s' % path, 'name': u'Slovenčina'})

    if settings.LANGUAGE_CODE != 'fr-fr':
        langs.append({'url': 'http://fr.wammu.eu%s' % path, 'name': u'Français'})

    return {'translations': langs}

def menu(request):
    return {'menu': [
            {'title': _('Support'), 'link': '/support/'},
            {'title': _('Download'), 'link': '/download/'},
            {'title': _('Screenshots'), 'link': '/screenshots/'},
            {'title': _('Documentation'), 'link': '/docs/'},
            {'title': _('Contribute'), 'link': '/contribute/'},
            {'title': _('Tools'), 'link': '/tools/'},
            ]}

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
