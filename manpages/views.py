from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy, ugettext as _

from django.conf import settings

from django.http import Http404

import os

langnames = {
    'cs': ugettext_lazy('Czech'),
    'en': ugettext_lazy('English'),
    'en_GB': ugettext_lazy('English (Great Britain)'),
    'de': ugettext_lazy('German'),
    'fr': ugettext_lazy('French'),
    'it': ugettext_lazy('Italian'),
    'nl': ugettext_lazy('Dutch'),
    'sk': ugettext_lazy('Slovak'),
    'ru': ugettext_lazy('Russian'),
}

langparts = settings.LANGUAGE_CODE.split('-')
if len(langparts) == 1:
    globallang = langparts[0]
else:
    globallang = '%s_%s' % (langparts[0], langparts[1].upper)
    if not langnames.has_key(globallang):
        globallang = langparts[0]
del langparts
if not langnames.has_key(globallang):
    raise Exception('Bad language: %s' % globallang)

def langcmp(a, b):
    if a == globallang:
        return -1
    if b == globallang:
        return 1
    return cmp(a, b)

# Create your views here.

def show_page(request, page, lang = 'en'):
    if not langnames.has_key(lang):
        raise Http404('Language not found!')
    manpage = 'docs/man/%s/%s.html' % (lang, page)
    message = None
    if not os.path.exists('%s/%s' % (settings.HTML_ROOT, manpage)):
        lang = 'en'
        message = _('This man page is not translated to selected language, displaying English version instead.')
        manpage = 'docs/man/%s/%s.html' % (lang, page)
    return render_to_response('docs/show_man.html', RequestContext(request, {
        'manpage': manpage,
        'message': message,
        'lang': lang,
        'page': page,
        'others': list_pages(lang),
    }))

def list_langs():
    ret = os.listdir('%s/docs/man' % settings.HTML_ROOT)
    ret.sort(cmp = langcmp)
    return ret

def list_pages(lang = 'en'):
    ret = [x[:-5] for x in os.listdir('%s/docs/man/%s' % (settings.HTML_ROOT, lang))]
    ret.sort()
    return ret

def list_lang_mans():
    langs = list_langs()
    return [(lang, langnames[lang], list_pages(lang)) for lang in langs]

def show_pages(request):
    return render_to_response('docs/list_man.html', RequestContext(request, {
        'manpages': list_lang_mans(),
    }))


def show_lang_pages(request, lang):
    if not langnames.has_key(lang):
        raise Http404('Language not found!')
    return render_to_response('docs/list_man.html', RequestContext(request, {
        'manpages': [('.', langnames[lang], list_pages(lang))],
    }))

