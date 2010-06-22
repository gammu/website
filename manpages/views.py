from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy

from django.conf import settings

from django.http import Http404

import os

langnames = {
    'cs': ugettext_lazy('Czech'),
    'en': ugettext_lazy('English'),
    'de': ugettext_lazy('German'),
    'it': ugettext_lazy('Italian'),
    'nl': ugettext_lazy('Dutch'),
    'sk': ugettext_lazy('Slovak'),
}

def langcmp(a, b):
    if a == 'en':
        return -1
    if b == 'en':
        return 1
    return cmp(a, b)

# Create your views here.

def show_page(request, page, lang = 'en'):
    manpage = 'docs/man/%s/%s.html' % (lang, page)
    if not os.path.exists('%s/%s' % (settings.HTML_ROOT, manpage)):
        raise Http404('No man page matching %s/%s found.' % (lang, page))
    return render_to_response('docs/show_man.html', RequestContext(request, {
        'manpage': manpage,
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

