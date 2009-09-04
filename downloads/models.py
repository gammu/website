from django.db import models

from wammu_web.news.models import Entry, Category

from django.contrib.auth.models import User

import markdown

import os

from wammu_web.wammu.helpers import process_bug_links

PROGRAM_CHOICES = (
    ('gammu', 'Gammu'),
    ('wammu', 'Wammu'),
    ('python-gammu', 'python-gammu'),
    )

PROGRAM_URLS = {
    'gammu': '/gammu/',
    'wammu': '/wammu/',
    'python-gammu': '/python-gammu/',
}

PLATFORM_CHOICES = (
    ('source', 'Source'),
    ('win32', 'Windows binary'),
    )

def get_latest_releases(program):
    '''
    Returns tuple with last release information for given program.
    First is stable, second is testing, which can be None.
    '''
    releases = Release.objects.filter(program = program)
    latest_version = releases.order_by('-version_int')[0]
    if latest_version.version_int % 100 < 10:
        latest_stable = latest_version
        latest_testing = None
    else:
        latest_testing = latest_version
        latest_stable = releases.filter(version_int__lt = 10 + ((latest_version.version_int / 100) * 100)).order_by('-version_int')[0]
    return (latest_stable, latest_testing)

def get_program(name):
    for c in PROGRAM_CHOICES:
        if c[0] == name:
            return c[1]
    raise IndexError('Program does not exist!')

def get_current_downloads(program, platform = 'source'):
    '''
    Gets list of tuples for currently active downloads. The first one
    is always present and it's the stable one, the second one is
    testing if available.
    '''

    downloads = []

    stable_release, testing_release = get_latest_releases(program)

    stable_downloads = Download.objects.filter(release = stable_release, platform = platform).order_by('location')

    downloads.append((stable_release, stable_downloads))

    if testing_release is not None:
        testing_downloads = Download.objects.filter(release = testing_release, platform = platform).order_by('location')
        downloads.append((testing_release, testing_downloads))

    return downloads


class Mirror(models.Model):
    name = models.CharField(max_length = 250)
    slug = models.SlugField(unique = True)
    url = models.CharField(max_length = 250)

    def __unicode__(self):
        return self.name


class Release(models.Model):
    author = models.ForeignKey(User)
    program = models.CharField(max_length = 100, choices = PROGRAM_CHOICES)
    version = models.CharField(max_length = 100)
    version_int = models.IntegerField(editable = False, blank = True)
    description = models.TextField()
    description_html = models.TextField(editable = False, blank = True)
    changelog = models.TextField(blank = True, null = True)
    changelog_html = models.TextField(blank = True, null = True, editable = False)
    date = models.DateTimeField(auto_now_add = True)
    post_news = models.BooleanField(default = True)
    post_tweet = models.BooleanField(default = True)

    def save(self):
        version = self.version.split('.')
        self.version_int = 0
        for num in version:
            self.version_int = (100 * self.version_int) + int(num)
        # Implicit .0
        if len(version) == 2:
            self.version_int = 100 * self.version_int
        if self.post_news:
            author = self.author
            excerpt = '[%s][1] [%s][2] has been just released. %s\n\n[1]: %s\n[2]:%s' % (
                get_program(self.program),
                self.version,
                self.description,
                PROGRAM_URLS[self.program],
                self.get_absolute_url(),
                )
            body = 'Full list of changes:\n\n%s\n\nYou can download it from <http://wammu.eu/download/>.' % self.changelog
            identica_post = self.post_tweet
            identica_text = '#%s %s has been just released' % (
                get_program(self.program),
                self.version,
                )
            title = '%s %s' % (
                get_program(self.program),
                self.version,
                )
            slug = '%s-%s' % (
                self.program,
                self.version,
                )
            category = Category.objects.get(slug = self.program)
            entry = category.entry_set.create(
                author = author,
                excerpt = excerpt,
                body = process_bug_links(body),
                identica_post = identica_post,
                identica_text = identica_text,
                title = title,
                slug = slug,
                )
        self.post_news = False
        self.post_tweet = False
        self.changelog_html = markdown.markdown(process_bug_links(self.changelog))
        self.description_html = markdown.markdown(self.description)
        super(Release, self).save()

    def __unicode__(self):
        return '%s-%s' % (self.program, self.version)

    def get_state(self):
        if self.program == 'gammu' and self.version_int % 100 > 90:
            return 'testing release %s' % self.version
        else:
            return 'stable release %s' % self.version

    def get_program(self):
        return get_program(self.program)

    @models.permalink
    def get_absolute_url(self):
         return ('downloads.views.release', (), { 'version': self.version, 'program': self.program })


class Download(models.Model):
    release = models.ForeignKey(Release)
    platform = models.CharField(max_length = 100, choices = PLATFORM_CHOICES)
    location = models.CharField(max_length = 250)
    md5 = models.CharField(max_length = 250)
    sha1 = models.CharField(max_length = 250)
    size = models.IntegerField()

    def __unicode__(self):
        return '%s (%s): %s' % (self.release.__unicode__(), self.platform, self.location)

    def get_filename(self):
        return os.path.split(self.location)[1]

    def get_size(self):
        if self.size > 4 * 1024 * 1024:
            return '%d MiB' % (self.size / (1024 * 1024))
        if self.size > 4 * 1024:
            return '%d kiB' % (self.size / 1024)
        return '%d B' % self.size
