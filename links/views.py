from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from links.models import Link

from django.conf import settings


# Create your views here.

def index(request):
    objects = Link.objects.order_by('title')

    return render_to_response('links/index.html', RequestContext(request, {
        'links': objects,
    }))
