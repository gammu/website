from django.shortcuts import render_to_response, get_object_or_404
from wammu_web.wammu.helpers import WammuContext
from downloads.models import Download, Release, Mirror, get_program, get_latest_releases, get_current_downloads, PLATFORM_CHOICES
from django.http import Http404
from django.utils.datastructures import MultiValueDictKeyError

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

    downloads = get_current_downloads(program, platform)

    stable_release, stable_downloads = downloads[0]
    try:
        testing_release, testing_downloads = downloads[1]
    except IndexError:
        testing_release, testing_downloads = (None, None)

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

def release(request, program,  version):

    release = get_object_or_404(Release, program = program, version = version)
    downloads = Download.objects.filter(release = release).order_by('location')

    if downloads.count() == 0:
        raise Http404('No such download option %s/%s.' % (program, version))

    mirror, mirrors, set_mirror, mirror_id = get_mirrors(request)

    result = render_to_response('downloads/release.html', WammuContext(request, {
        'release': release,
        'downloads': downloads,
        'program': get_program(program),
        'mirrors': mirrors,
        'mirror': mirror,
    }))
    if set_mirror:
        result.set_cookie('mirror', mirror_id, max_age = 3600 * 24 * 365)
    return result


def program(request, program):

    stable_release, testing_release = get_latest_releases(program)

    mirror, mirrors, set_mirror, mirror_id = get_mirrors(request)

    return render_to_response('downloads/program.html', WammuContext(request, {
        'stable_release': stable_release,
        'testing_release': testing_release,
        'platforms': PLATFORM_CHOICES,
        'program': get_program(program),
        'program_name': program,
        'mirrors': mirrors,
        'mirror': mirror,
    }))
