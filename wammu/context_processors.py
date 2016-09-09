# Context processors
# -*- coding: UTF-8 -*-

from django.conf import settings
from datetime import datetime
from django.utils.translation import ugettext as _, get_language
from news.models import Category
from screenshots.models import Category as ScreenshotCategory


def translations(request):
    path = request.get_full_path()
    langs = []

    lang = get_language()

    if lang != 'cs':
        langs.append({'url': 'https://cs.wammu.eu%s' % path, 'name': u'Česky', 'code': 'cs'})

    if lang != 'en':
        langs.append({'url': 'https://wammu.eu%s' % path, 'name': u'English', 'code': 'en'})

    if lang != 'es':
        langs.append({'url': 'https://es.wammu.eu%s' % path, 'name': u'Español', 'code': 'es'})

    if lang != 'de':
        langs.append({'url': 'https://de.wammu.eu%s' % path, 'name': u'Deutsch', 'code': 'de'})

    if lang != 'sk':
        langs.append({'url': 'https://sk.wammu.eu%s' % path, 'name': u'Slovenčina', 'code': 'sk'})

    if lang != 'fr':
        langs.append({'url': 'https://fr.wammu.eu%s' % path, 'name': u'Français', 'code': 'fr'})

    if lang != 'pt-br':
        langs.append({'url': 'https://pt-br.wammu.eu%s' % path, 'name': u'Português brasileiro', 'code': 'pt-BR'})

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
    }

def feeds(request):
    return {'global_feeds': [
            {'url': '/news/rss/', 'title': _('Gammu and Wammu News Feed (RSS)'), 'type': 'application/rss+xml'},
            {'url': '/news/atom/', 'title': _('Gammu and Wammu News Feed (Atom)'), 'type': 'application/atom+xml'},
    ]}


def data(request):
    return {
        'news_categories': Category.objects.all(),
        'screenshot_categories': ScreenshotCategory.objects.all(),
    }
