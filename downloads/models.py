from django.db import models

PROGRAM_CHOICES = (
    ('gammu', 'Gammu'),
    ('wammu', 'Wammu'),
    ('python-gammu', 'python-gammu'),
    )

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

class Download(models.Model):
    release = models.CharField(max_length = 100)
    release_int = models.IntegerField(editable = False, blank = True)
    program = models.CharField(max_length = 100, choices = PROGRAM_CHOICES)
    platform = models.CharField(max_length = 100, choices = PLATFORM_CHOICES)
    location = models.CharField(max_length = 250)
    md5 = models.CharField(max_length = 250)
    size = models.IntegerField()
    released = models.DateTimeField(auto_now_add = True)

    def __unicode__(self):
        return '%s-%s (%s): %s' % (self.program, self.release, self.platform, self.location)

    def save(self):
        release = self.release.split('.')
        self.release_int = 0
        for num in release:
            self.release_int = (100 * self.release_int) + int(num)
        super(Download, self).save()

    def get_state(self):
        if self.program == 'gammu' and self.release_int % 100 > 90:
            return 'Testing release'
        else:
            return 'Stable release'
