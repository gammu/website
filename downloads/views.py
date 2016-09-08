from django.shortcuts import render_to_response, get_object_or_404, redirect, render
from django.template import RequestContext
from downloads.models import Download, Release, get_program, get_latest_releases, get_current_downloads, PLATFORM_CHOICES, PROGRAM_CHOICES
from django.http import Http404, HttpResponse


def detail(request, program):
    if not program in [x[0] for x in PROGRAM_CHOICES]:
        raise Http404('No such program %s.' % program)

    downloads = get_current_downloads(program)

    stable_release, stable_downloads = downloads[0]
    try:
        testing_release, testing_downloads = downloads[1]
    except IndexError:
        testing_release, testing_downloads = (None, None)

    if stable_downloads.count() == 0:
        raise Http404('No such download option %s.' % program)

    platform = 'source'
    for c in PLATFORM_CHOICES:
        if platform == c[0]:
            platform_name = c[1]

    result = render_to_response('downloads/detail.html', RequestContext(request, {
        'stable_release': stable_release,
        'testing_release': testing_release,
        'stable_downloads': stable_downloads,
        'testing_downloads': testing_downloads,
        'program_include': 'downloads/programs/%s-%s.html' % (program, platform),
        'program': get_program(program),
        'program_name': program,
        'platform': platform_name,
    }))
    return result

def release(request, program,  version):

    release = get_object_or_404(Release, program = program, version = version)
    downloads = Download.objects.filter(release = release).order_by('location')

    if downloads.count() == 0:
        raise Http404('No such download option %s/%s.' % (program, version))

    result = render_to_response('downloads/release.html', RequestContext(request, {
        'release': release,
        'downloads': downloads,
        'program': get_program(program),
        'program_name': program,
    }))
    return result


def download(request):
    return render(request, 'downloads/index.html')


def doap(request, program):
    if not program in [x[0] for x in PROGRAM_CHOICES]:
        raise Http404('No such program %s.' % program)

    downloads = get_current_downloads(program)

    return render_to_response('downloads/doap/%s.xml' % program, RequestContext(request, {
        'downloads': downloads[0][1],
        'release': downloads[0][0],
    }), content_type = 'application/xml')

def pad(request, program):
    if not program in [x[0] for x in PROGRAM_CHOICES]:
        raise Http404('No such program %s.' % program)

    downloads = get_current_downloads(program)

    release = downloads[0][0]
    download = downloads[0][1].filter(location__iendswith='.zip')[0]

    return render_to_response('downloads/pad/%s.xml' % program, RequestContext(request, {
        'download': download,
        'release': release,
    }), content_type = 'application/xml')

def padmap(request):
    '''
    Public list of PAD files.
    '''
    response = HttpResponse(content_type='text/plain')
    response.write('https://wammu.eu/api/pad/gammu.xml\n')
    response.write('https://wammu.eu/api/pad/wammu.xml\n')
    return response
