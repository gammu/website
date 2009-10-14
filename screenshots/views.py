from django.shortcuts import render_to_response, get_object_or_404
from wammu.helpers import WammuContext
from screenshots.models import Screenshot, Category

from django.core.paginator import Paginator, InvalidPage, EmptyPage

from django.conf import settings


# Create your views here.

def index(request):
    objects = Screenshot.objects.order_by('title')
    return render_screenshots(request, objects, 'screenshots/index.html')

def category(request, slug):
    category = get_object_or_404(Category, slug = slug)
    objects = Screenshot.objects.filter(categories = category).order_by('title')
    return render_screenshots(request, objects, 'screenshots/%s_index.html' % slug)

def render_screenshots(request, objects, template):
    paginator = Paginator(objects, settings.SCREENSHOTS_PER_PAGE, orphans = 2)
    try:
        page = int(request.GET.get('page', '1'))
        if page < 1:
            page = 0
        elif page > paginator.num_pages:
            page = paginator.num_pages
    except ValueError:
        page = 1

    try:
        screenshots = paginator.page(page)
    except (EmptyPage, InvalidPage):
        screenshots = paginator.page(1)

    screenshots_categories = Category.objects.order_by('slug')

    return render_to_response(template, WammuContext(request, {
        'screenshots': screenshots,
        'screenshots_categories': screenshots_categories,
    }))
