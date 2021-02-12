from django.conf import settings
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.shortcuts import get_object_or_404, render

from screenshots.models import Category, Screenshot

# Create your views here.


def index(request):
    objects = Screenshot.objects.order_by("title")
    return render_screenshots(request, objects, "screenshots/index.html")


def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    objects = Screenshot.objects.filter(categories=category).order_by("title")
    return render_screenshots(request, objects, "screenshots/%s_index.html" % slug)


def render_screenshots(request, objects, template):
    paginator = Paginator(objects, settings.SCREENSHOTS_PER_PAGE, orphans=2)
    try:
        page = int(request.GET.get("page", "1"))
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

    return render(
        request,
        template,
        {
            "screenshots": screenshots,
        },
    )
