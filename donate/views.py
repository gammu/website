from django.shortcuts import render_to_response, get_object_or_404
from wammu_web.wammu.helpers import WammuContext

from django.conf import settings

def donate(request):
    return render_to_response('donate.html', WammuContext(request, {
    }))

def thanks(request):
    return render_to_response('donate-thanks.html', WammuContext(request, {
    }))

