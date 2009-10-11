from django.shortcuts import render_to_response
from wammu.helpers import WammuContext
from news.models import Entry, Category
from screenshots.models import Screenshot
from downloads.models import Release
from phonedb.models import Phone
from downloads.models import Download, Release, Mirror, get_current_downloads
from downloads.views import get_mirrors

from django.conf import settings

from django.contrib.sites.models import Site, RequestSite
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
    category = Category.objects.get(slug = 'wammu')
    news = Entry.objects.filter(categories = category).order_by('-pub_date')[:settings.NEWS_ON_PRODUCT_PAGE]
    return render_to_response('wammu.html', WammuContext(request, {
        'news': news,
        'news_category': category,
    }))

def smsd(request):
    category = Category.objects.get(slug = 'gammu')
    news = Entry.objects.filter(categories = category).order_by('-pub_date')[:settings.NEWS_ON_PRODUCT_PAGE]
    return render_to_response('smsd.html', WammuContext(request, {
        'news': news,
        'news_category': category,
    }))

def gammu(request):
    category = Category.objects.get(slug = 'gammu')
    news = Entry.objects.filter(categories = category).order_by('-pub_date')[:settings.NEWS_ON_PRODUCT_PAGE]
    return render_to_response('gammu.html', WammuContext(request, {
        'news': news,
        'news_category': category,
    }))

def pygammu(request):
    category = Category.objects.get(slug = 'gammu')
    news = Entry.objects.filter(categories = category).order_by('-pub_date')[:settings.NEWS_ON_PRODUCT_PAGE]
    return render_to_response('python-gammu.html', WammuContext(request, {
        'news': news,
        'news_category': category,
    }))

def libgammu(request):
    category = Category.objects.get(slug = 'gammu')
    news = Entry.objects.filter(categories = category).order_by('-pub_date')[:settings.NEWS_ON_PRODUCT_PAGE]
    return render_to_response('libgammu.html', WammuContext(request, {
        'news': news,
        'news_category': category,
    }))

def static(request, page):
    return render_to_response(page, WammuContext(request, {
    }))

def robots(request):
    if Site._meta.installed:
        current_site = Site.objects.get_current()
    else:
        current_site = RequestSite(self.request)
    return render_to_response('robots.txt', WammuContext(request, {
        'current_site': current_site,
    }), mimetype = 'text/plain')
