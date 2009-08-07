from django.db import models

class Mirror(models.Model):
    name = models.CharField(max_length = 250)
    slug = models.SlugField(unique = True)
    url = models.CharField(max_length = 250)

    def __unicode__(self):
        return self.name


class Program(models.Model):
    name = models.CharField(max_length = 250)
    slug = models.SlugField(unique = True)
    url = models.CharField(max_length = 200)

    def __unicode__(self):
        return self.name

class ReleaseType(models.Model):
    name = models.CharField(max_length = 250)

    def __unicode__(self):
        return self.name

class Release(models.Model):
    program = models.ForeignKey(Program)
    version = models.CharField(max_length = 100)
    type = models.ForeignKey(ReleaseType)

    def __unicode__(self):
        return '%s %s' % (self.program.name, self.version)

class DownloadKind(models.Model):
    name = models.CharField(max_length = 250)

    def __unicode__(self):
        return self.name

class DownloadType(models.Model):
    name = models.CharField(max_length = 250)
    kind = models.ForeignKey(DownloadKind)

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.kind.name)

class Download(models.Model):
    location = models.CharField(max_length = 250)
    release = models.ForeignKey(Release)
    type = models.ForeignKey(DownloadType)
    md5 = models.CharField(max_length = 250)

    def __unicode__(self):
        return self.location
