from django.shortcuts import render_to_response
from wammu_web.wammu.helpers import WammuContext
from wammu_web.news.models import Entry
from wammu_web.screenshots.models import Screenshot
from wammu_web.downloads.models import Release
from wammu_web.phonedb.models import Phone
from downloads.models import Download, Release, Mirror, get_current_downloads
from downloads.views import get_mirrors

from django.conf import settings

# Create your views here.

def index(request):
    mirror, mirrors, set_mirror, mirror_id = get_mirrors(request)

    downloads = get_current_downloads('gammu', 'source')
    downloads += get_current_downloads('wammu', 'source')

    news = Entry.objects.order_by('-pub_date')[:settings.NEWS_ON_MAIN_PAGE]
    screenshot = Screenshot.objects.filter(featured = True).order_by('?')[0]
    phones = Phone.objects.filter(state__in = ['approved', 'draft']).order_by('-created')[:settings.PHONES_ON_MAIN_PAGE]
    return render_to_response('index.html', WammuContext(request, {
        'news': news,
        'screenshot': screenshot,
        'downloads': downloads,
        'mirror': mirror,
        'phones': phones,
    }))

def wammu(request):
    return render_to_response('wammu.html', WammuContext(request, {
    }))

def smsd(request):
    return render_to_response('smsd.html', WammuContext(request, {
    }))

def gammu(request):
    return render_to_response('gammu.html', WammuContext(request, {
    }))

def pygammu(request):
    return render_to_response('python-gammu.html', WammuContext(request, {
    }))

def libgammu(request):
    return render_to_response('libgammu.html', WammuContext(request, {
    }))

def static(request, page):
    return render_to_response(page, WammuContext(request, {
    }))
