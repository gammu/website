from django.shortcuts import render_to_response, get_object_or_404
from wammu_web.wammu.helpers import WammuContext
from downloads.models import Download, Release, Mirror, get_program
from django.http import Http404
from django.utils.datastructures import MultiValueDictKeyError

def get_latest_releases(program):
    releases = Release.objects.filter(program = program)
    latest_version = releases.order_by('-version_int')[0]
    if latest_version.version_int % 100 < 10:
        latest_stable = latest_version
        latest_testing = None
    else:
        latest_testing = latest_version
        latest_stable = releases.filter(version_int__lt = 10 + ((latest_version.version_int / 100) * 100)).order_by('-version_int')[0]
    return (latest_stable, latest_testing)

def get_mirrors(request):
    mirrors = Mirror.objects.all().order_by('id')
    set_mirror = False
    try:
        try:
            mirror_id = request.GET['mirror']
        except (MultiValueDictKeyError, KeyError):
            mirror_id = request.COOKIES['mirror']
        set_mirror = True
    except (MultiValueDictKeyError, KeyError):
        mirror_id = 'cihar-com'
    try:
        mirror = Mirror.objects.get(slug = mirror_id)
    except Mirror.DoesNotExist:
        mirror = Mirror.objects.get(slug = 'cihar-com')

    return (mirror, mirrors, set_mirror, mirror_id)

def list(request, program, platform):

    stable_release, testing_release = get_latest_releases(program)

    stable_downloads = Download.objects.filter(release = stable_release, platform = platform).order_by('location')

    if testing_release is None:
        testing_downloads = None
    else:
        testing_downloads = Download.objects.filter(release = testing_release, platform = platform).order_by('location')

    if stable_downloads.count() == 0:
        raise Http404('No such download option %s/%s.' % (program, platform))

    mirror, mirrors, set_mirror, mirror_id = get_mirrors(request)

    result = render_to_response('downloads/list.html', WammuContext(request, {
        'stable_release': stable_release,
        'testing_release': testing_release,
        'stable_downloads': stable_downloads,
        'testing_downloads': testing_downloads,
        'program_include': 'downloads/programs/%s-%s.html' % (program, platform),
        'program': get_program(program),
        'mirrors': mirrors,
        'mirror': mirror,
    }))
    if set_mirror:
        result.set_cookie('mirror', mirror_id, max_age = 3600 * 24 * 365)
    return result
