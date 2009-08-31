from django.db import models

from wammu_web.news.models import Entry, Category

from django.contrib.auth.models import User

PROGRAM_CHOICES = (
    ('gammu', 'Gammu'),
    ('wammu', 'Wammu'),
    ('python-gammu', 'python-gammu'),
    )

PROGRAM_URLS = {
    'gammu': 'http://wammu.eu/gammu/',
    'wammu': 'http://wammu.eu/wammu/',
    'python-gammu': 'http://wammu.eu/python-gammu/',
}

PLATFORM_CHOICES = (
    ('source', 'Source'),
    ('win32', 'Windows binary'),
    )

def get_program(name):
    for c in PROGRAM_CHOICES:
        if c[0] == name:
            return c[1]
    raise IndexError('Program does not exist!')

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
        if self.post_news:
            author = self.author
            excerpt = '[%s][1] %s has been just released. %s\n\n[1]: %s' % (
                get_program(self.program),
                self.version,
                self.description,
                PROGRAM_URLS[self.program],
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
                body = body,
                identica_post = identica_post,
                identica_text = identica_text,
                title = title,
                slug = slug,
                )
        self.post_news = False
        self.post_tweet = False
        super(Release, self).save()

    def __unicode__(self):
        return '%s-%s' % (self.program, self.version)

    def get_state(self):
        if self.program == 'gammu' and self.release_int % 100 > 90:
            return 'Testing release %s' % self.release
        else:
            return 'Stable release %s' % self.release

    def get_program(self):
        return get_program(self.program)


class Download(models.Model):
    release = models.ForeignKey(Release)
    platform = models.CharField(max_length = 100, choices = PLATFORM_CHOICES)
    location = models.CharField(max_length = 250)
    md5 = models.CharField(max_length = 250)
    sha1 = models.CharField(max_length = 250)
    size = models.IntegerField()

    def __unicode__(self):
        return '%s (%s): %s' % (self.release.__unicode__(), self.platform, self.location)

