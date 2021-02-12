from django.shortcuts import render

from links.models import Link


def index(request):
    objects = Link.objects.order_by("title")

    return render(request, "links/index.html", {"links": objects})
