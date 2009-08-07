from django.shortcuts import render_to_response
from wammu_web.wammu.helpers import WammuContext
from wammu_web.news.models import Entry

# Create your views here.

def index(request):
    news = Entry.objects.order_by('-pub_date')[:5]
    return render_to_response('index.html', WammuContext(request, {
        'news': news,
    }))

def gammu(request):
    return render_to_response('gammu.html', WammuContext(request, {
    }))

def pygammu(request):
    return render_to_response('python-gammu.html', WammuContext(request, {
    }))

def libgammu(request):
    return render_to_response('libgammu.html', WammuContext(request, {
    }))
