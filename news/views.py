from django.conf import settings
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.shortcuts import get_object_or_404, render

from news.models import Category, Entry

# Create your views here.


def entry(request, slug, day=None, month=None, year=None):
    entry = get_object_or_404(Entry, slug=slug)
    return render(
        request,
        "news/entry.html",
        {
            "entry": entry,
        },
    )


def index(request):
    objects = Entry.objects.order_by("-pub_date").prefetch_related("author")
    return render_news(request, objects, "news/index.html")


def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    objects = (
        Entry.objects.filter(categories=category)
        .order_by("-pub_date")
        .prefetch_related("author")
    )
    return render_news(request, objects, f"news/{slug}_index.html")


def render_news(request, objects, template):
    paginator = Paginator(objects, settings.NEWS_PER_PAGE, orphans=1)
    try:
        page = int(request.GET.get("page", "1"))
        if page < 1:
            page = 0
        elif page > paginator.num_pages:
            page = paginator.num_pages
    except ValueError:
        page = 1

    try:
        news = paginator.page(page)
    except (EmptyPage, InvalidPage):
        news = paginator.page(1)

    return render(
        request,
        template,
        {
            "news": news,
        },
    )
