from django.shortcuts import render, get_object_or_404
from downloads.models import Download, Release, get_program, get_current_downloads, PROGRAM_CHOICES
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

    return render(request, 'downloads/detail.html', {
        'stable_release': stable_release,
        'testing_release': testing_release,
        'stable_downloads': stable_downloads,
        'testing_downloads': testing_downloads,
        'program': get_program(program),
        'program_name': program,
    })

def release(request, program,  version):

    release = get_object_or_404(Release, program = program, version = version)
    downloads = Download.objects.filter(release = release)

    if downloads.count() == 0:
        raise Http404('No such download option %s/%s.' % (program, version))

    return render(request, 'downloads/release.html', {
        'release': release,
        'downloads': downloads,
        'program': get_program(program),
        'program_name': program,
    })


def download(request):
    return render(request, 'downloads/index.html')


def doap(request, program):
    if not program in [x[0] for x in PROGRAM_CHOICES]:
        raise Http404('No such program %s.' % program)

    downloads = get_current_downloads(program)

    return render(request, 'downloads/doap/%s.xml' % program, {
        'downloads': downloads[0][1],
        'release': downloads[0][0],
    }, content_type = 'application/xml')


def pad(request, program):
    if not program in [x[0] for x in PROGRAM_CHOICES]:
        raise Http404('No such program %s.' % program)

    downloads = get_current_downloads(program)

    release = downloads[0][0]
    try:
        download = downloads[0][1].filter(location__iendswith='windows.exe')[0]
    except IndexError:
        download = downloads[0][1].filter(location__iendswith='.zip')[0]

    return render(request, 'downloads/pad/%s.xml' % program, {
        'download': download,
        'release': release,
    }, content_type = 'application/xml')

def padmap(request):
    '''
    Public list of PAD files.
    '''
    response = HttpResponse(content_type='text/plain')
    response.write('https://wammu.eu/api/pad/gammu.xml\n')
    response.write('https://wammu.eu/api/pad/wammu.xml\n')
    return response
