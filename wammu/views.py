from django.shortcuts import render_to_response
from wammu_web.wammu.helpers import WammuContext
from wammu_web.news.models import Entry
from wammu_web.screenshots.models import Screenshot
from wammu_web.downloads.models import Release
from downloads.models import Download, Release, Mirror, get_program
from downloads.views import get_mirrors, get_latest_releases

# Create your views here.

def index(request):
    mirror, mirrors, set_mirror, mirror_id = get_mirrors(request)

    gammu_stable_release, gammu_testing_release = get_latest_releases('gammu')

    gammu_stable_downloads = Download.objects.filter(release = gammu_stable_release, platform = 'source').order_by('location')

    if gammu_testing_release is None:
        gammu_testing_downloads = None
    else:
        gammu_testing_downloads = Download.objects.filter(release = gammu_testing_release, platform = 'source').order_by('location')

    news = Entry.objects.order_by('-pub_date')[:5]
    screenshot = Screenshot.objects.filter(featured = True).order_by('?')[0]
    return render_to_response('index.html', WammuContext(request, {
        'news': news,
        'screenshot': screenshot,
        'gammu_stable_release': gammu_stable_release,
        'gammu_testing_release': gammu_testing_release,
        'gammu_stable_downloads': gammu_stable_downloads,
        'gammu_testing_downloads': gammu_testing_downloads,
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
