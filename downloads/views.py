from django.shortcuts import render_to_response, get_object_or_404
from wammu_web.wammu.helpers import WammuContext
from downloads.models import Download, Mirror, get_program
from django.http import Http404

def list(request, program, platform):
    downloads = Download.objects.filter(program = program, platform = platform).order_by('location')
    if downloads.count() == 0:
        raise Http404('No such download option %s/%s.' % (program, platform))

    return render_to_response('downloads/list.html', WammuContext(request, {
        'downloads': downloads,
        'program': get_program(program),
    }))

