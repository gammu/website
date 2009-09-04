from django.shortcuts import render_to_response, get_object_or_404
from wammu_web.wammu.helpers import WammuContext
# Create your views here.

def show_page(request, page, lang = 'en'):
    manpage = 'docs/man/%s/%s.html' % (lang, page)
    return render_to_response('docs/show_man.html', WammuContext(request, {
        'manpage': manpage,
        'title': page,
    }))
