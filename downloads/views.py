from django.shortcuts import render_to_response, get_object_or_404
from wammu_web.wammu.helpers import WammuContext
from downloads.models import Download, Mirror, get_program
from django.http import Http404
from django.utils.datastructures import MultiValueDictKeyError

def list(request, program, platform):
    downloads = Download.objects.filter(program = program, platform = platform)
    if downloads.count() == 0:
        raise Http404('No such download option %s/%s.' % (program, platform))
    # Get latest release
    latest = downloads.order_by('release_int')[0]
    # Limit us only on latest major version + testing one
    limit = (latest.release_int / 100) * 100
    downloads = downloads.filter(release_int__gte = limit).order_by('location')
    mirrors = Mirror.objects.all().order_by('id')
    set_mirror = False
    try:
        try:
            mirror_id = request.GET['mirror']
        except MultiValueDictKeyError:
            mirror_id = request.COOKIES['mirror']
        set_mirror = True
    except MultiValueDictKeyError:
        mirror_id = 'cihar-com'
    try:
        mirror = Mirror.objects.get(slug = mirror_id)
    except Mirror.DoesNotExist:
        mirror = Mirror.objects.get(slug = 'cihar-com')

    result = render_to_response('downloads/list.html', WammuContext(request, {
        'downloads': downloads,
        'program_include': 'downloads/programs/%s-%s.html' % (program, platform),
        'program': get_program(program),
        'mirrors': mirrors,
        'mirror': mirror,
    }))
    if set_mirror:
        result.set_cookie('mirror', mirror_id, max_age = 3600 * 24 * 365)
    return result
