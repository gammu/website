from django.shortcuts import render_to_response
from django.template import RequestContext
from news.models import Entry, Category
from screenshots.models import Screenshot
from phonedb.models import Phone
from downloads.models import get_current_downloads, get_latest_releases
from downloads.views import get_mirrors

from django.conf import settings

from django.contrib.sites.models import Site, RequestSite
# Create your views here.

def process_version_feedback(request):
    '''
    Handles feedback from Wammu, which includes version URL parameter. Return
    value is dictionary to be fed to rendering context.
    '''
    result = {'feedback': False}
    if request.GET.has_key('version'):
        result['feedback'] = True
        version = request.GET['version']
        last_rel, testing_rel = get_latest_releases('wammu')
        if last_rel.version != version:
            result['update_release'] = last_rel
    return result

def index(request):
    mirror, mirrors, set_mirror, mirror_id = get_mirrors(request)

    downloads = get_current_downloads('gammu', 'source')
    downloads += get_current_downloads('wammu', 'source')

    news = Entry.objects.order_by('-pub_date')[:settings.NEWS_ON_MAIN_PAGE]
    screenshot = Screenshot.objects.filter(featured = True).order_by('?')[0]
    phones = Phone.objects.filter(state__in = ['approved', 'draft']).order_by('-created')[:settings.PHONES_ON_MAIN_PAGE]
    return render_to_response('index.html', RequestContext(request, {
        'news': news,
        'screenshot': screenshot,
        'downloads': downloads,
        'mirror': mirror,
        'phones': phones,
    }))

def support(request):
    context  = process_version_feedback(request)
    return render_to_response('support/index.html', RequestContext(request, context))

def wammu(request):
    category = Category.objects.get(slug = 'wammu')
    news = Entry.objects.filter(categories = category).order_by('-pub_date')[:settings.NEWS_ON_PRODUCT_PAGE]
    context  = process_version_feedback(request)
    context['news'] = news
    context['news_category'] = category
    return render_to_response('wammu.html', RequestContext(request, context))

def smsd(request):
    category = Category.objects.get(slug = 'gammu')
    news = Entry.objects.filter(categories = category).order_by('-pub_date')[:settings.NEWS_ON_PRODUCT_PAGE]
    return render_to_response('smsd.html', RequestContext(request, {
        'news': news,
        'news_category': category,
    }))

def gammu(request):
    category = Category.objects.get(slug = 'gammu')
    news = Entry.objects.filter(categories = category).order_by('-pub_date')[:settings.NEWS_ON_PRODUCT_PAGE]
    return render_to_response('gammu.html', RequestContext(request, {
        'news': news,
        'news_category': category,
    }))

def pygammu(request):
    category = Category.objects.get(slug = 'gammu')
    news = Entry.objects.filter(categories = category).order_by('-pub_date')[:settings.NEWS_ON_PRODUCT_PAGE]
    return render_to_response('python-gammu.html', RequestContext(request, {
        'news': news,
        'news_category': category,
    }))

def libgammu(request):
    category = Category.objects.get(slug = 'gammu')
    news = Entry.objects.filter(categories = category).order_by('-pub_date')[:settings.NEWS_ON_PRODUCT_PAGE]
    return render_to_response('libgammu.html', RequestContext(request, {
        'news': news,
        'news_category': category,
    }))

def static(request, page):
    return render_to_response(page, RequestContext(request, {
    }))

def robots(request):
    if Site._meta.installed:
        current_site = Site.objects.get_current()
    else:
        current_site = RequestSite(request)
    return render_to_response('robots.txt', RequestContext(request, {
        'current_site': current_site,
    }), mimetype = 'text/plain')
