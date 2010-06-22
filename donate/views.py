from django.shortcuts import render_to_response
from django.template import RequestContext

def donate(request):
    return render_to_response('donate.html', RequestContext(request, {
    }))

def thanks(request):
    return render_to_response('donate-thanks.html', RequestContext(request, {
    }))

