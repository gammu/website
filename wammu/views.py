from django.shortcuts import render
from news.models import Entry, Category
from screenshots.models import Screenshot
from phonedb.models import Phone
from downloads.models import get_latest_releases

from django.conf import settings

from django.contrib.sites.models import Site
# Create your views here.

def process_version_feedback(request):
    '''
    Handles feedback from Wammu, which includes version URL parameter. Return
    value is dictionary to be fed to rendering context.
    '''
    result = {'feedback': False}
    if 'version' in request.GET:
        result['feedback'] = True
        version = request.GET['version']
        last_rel = get_latest_releases('wammu')[0]
        if last_rel.version != version:
            result['update_release'] = last_rel
    return result

def index(request):
    news = Entry.objects.order_by('-pub_date')[:settings.NEWS_ON_MAIN_PAGE]
    try:
        screenshot = Screenshot.objects.filter(featured = True).order_by('?')[0]
    except IndexError:
        screenshot = None
    phones = Phone.objects.filter(state__in = ['approved', 'draft']).order_by('-created')[:settings.PHONES_ON_MAIN_PAGE]
    return render(request, 'index.html', {
        'news': news,
        'screenshot': screenshot,
        'phones': phones,
    })

def support(request):
    context  = process_version_feedback(request)
    return render(request, 'support/index.html', context)

def wammu(request):
    category = Category.objects.get(slug = 'wammu')
    news = Entry.objects.filter(categories = category).order_by('-pub_date')[:settings.NEWS_ON_PRODUCT_PAGE]
    context  = process_version_feedback(request)
    context['news'] = news
    context['news_category'] = category
    return render(request, 'wammu.html', context)

def smsd(request):
    category = Category.objects.get(slug = 'gammu')
    news = Entry.objects.filter(categories = category).order_by('-pub_date')[:settings.NEWS_ON_PRODUCT_PAGE]
    return render(request, 'smsd.html', {
        'news': news,
        'news_category': category,
    })

def gammu(request):
    category = Category.objects.get(slug = 'gammu')
    news = Entry.objects.filter(categories = category).order_by('-pub_date')[:settings.NEWS_ON_PRODUCT_PAGE]
    return render(request, 'gammu.html', {
        'news': news,
        'news_category': category,
    })

def pygammu(request):
    category = Category.objects.get(slug = 'python-gammu')
    news = Entry.objects.filter(categories = category).order_by('-pub_date')[:settings.NEWS_ON_PRODUCT_PAGE]
    return render(request, 'python-gammu.html', {
        'news': news,
        'news_category': category,
    })

def libgammu(request):
    category = Category.objects.get(slug = 'gammu')
    news = Entry.objects.filter(categories = category).order_by('-pub_date')[:settings.NEWS_ON_PRODUCT_PAGE]
    return render(request, 'libgammu.html', {
        'news': news,
        'news_category': category,
    })

def static(request, page):
    return render(request, page)

def robots(request):
    try:
        current_site = Site.objects.get_current(request)
    except Site.DoesNotExist:
        current_site = {'domain': 'wammu.eu'}
    return render(request, 'robots.txt', {
        'current_site': current_site,
    }, content_type = 'text/plain')
