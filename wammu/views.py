from django.shortcuts import render_to_response
from wammu_web.wammu.helpers import WammuContext

# Create your views here.

def index(request):
    return render_to_response('index.html', WammuContext(request, {
        'a': 'b'
    }))
