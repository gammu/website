from django.shortcuts import render_to_response, get_object_or_404
from wammu_web.wammu.helpers import WammuContext

from django.conf import settings

from django.http import Http404

import os

langnames = {
    'cs': 'Czech',
    'en': 'English',
}

# Create your views here.

def show_page(request, page, lang = 'en'):
    manpage = 'docs/man/%s/%s.html' % (lang, page)
    if not os.path.exists('%s/%s' % (settings.HTML_ROOT, manpage)):
        raise Http404('No man page matching %s/%s found.' % (lang, page))
    return render_to_response('docs/show_man.html', WammuContext(request, {
        'manpage': manpage,
        'page': page,
        'others': list_pages(lang),
    }))

def list_langs():
    ret = os.listdir('%s/docs/man' % settings.HTML_ROOT)
    ret.sort()
    return ret

def list_pages(lang = 'en'):
    ret = [x[:-5] for x in os.listdir('%s/docs/man/%s' % (settings.HTML_ROOT, lang))]
    ret.sort()
    return ret

def list_lang_mans():
    langs = list_langs()
    return [(lang, langnames[lang], list_pages(lang)) for lang in langs]

def show_pages(request):
    return render_to_response('docs/list_man.html', WammuContext(request, {
        'manpages': list_lang_mans(),
    }))


def show_lang_pages(request, lang):
    return render_to_response('docs/list_man.html', WammuContext(request, {
        'manpages': [('.', langnames[lang], list_pages(lang))],
    }))

