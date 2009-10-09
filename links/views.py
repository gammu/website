from django.shortcuts import render_to_response, get_object_or_404
from wammu.helpers import WammuContext
from links.models import Link

from django.conf import settings


# Create your views here.

def index(request):
    objects = Link.objects.order_by('title')

    return render_to_response('links/index.html', WammuContext(request, {
        'links': objects,
    }))
