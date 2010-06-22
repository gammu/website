from django.shortcuts import render_to_response
from wammu.helpers import WammuContext

def donate(request):
    return render_to_response('donate.html', WammuContext(request, {
    }))

def thanks(request):
    return render_to_response('donate-thanks.html', WammuContext(request, {
    }))

