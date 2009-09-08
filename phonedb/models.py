from django.db import models

import markdown

# Create your models here.

CONNECTION_CHOICES = (
    ('usb', 'USB'),
    ('serial', 'Serial'),
    ('irda', 'IrDA'),
    ('bluetooth', 'Bluetooth'),
    ('other', 'Other'),
    )

GARBLE_CHOICES = (
    ('atdot', 'atdot'),
    ('none', 'none'),
    ('hide', 'hide'),
    ('nospam', 'nospam'),
    )

STATE_CHOICES = (
    ('draft', 'Draft'),
    ('approved', 'Approved'),
    ('deleted', 'Deleted'),
    )


class Vendor(models.Model):
    name = models.CharField(max_length = 250)
    url = models.URLField(max_length = 250)
    slug = models.SlugField(unique = True)
    tuxmobil = models.SlugField(null = True)

    def __unicode__(self):
        return self.name

class Feature(models.Model):
    name = models.CharField(max_length = 250)

    def __unicode__(self):
        return self.name

class Connection(models.Model):
    name = models.CharField(max_length = 250)
    medium = models.CharField(max_length = 100, choices = CONNECTION_CHOICES)

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.medium)

class Phone(models.Model):
    name = models.CharField(max_length = 250)
    vendor = models.ForeignKey(Vendor)
    connection = models.ForeignKey(Connection, null = True)
    features = models.ManyToManyField(Feature, blank = True)
    model = models.CharField(max_length = 100, blank = True)
    gammu_version = models.CharField(max_length = 100, blank = True)
    note = models.TextField()
    note_html = models.TextField(editable = False, blank = True)
    author_name = models.CharField(max_length = 250, blank = True)
    author_email = models.EmailField(max_length = 250, blank = True)
    email_garble = models.CharField(max_length = 100, choices = GARBLE_CHOICES, default = 'atdot')
    state = models.CharField(max_length = 100, choices = STATE_CHOICES, db_index = True, default = 'draft')
    created = models.DateTimeField(auto_now_add = True)
    address = models.CharField(max_length = 100, blank = True)
    hostname = models.CharField(max_length = 100, blank = True)

    def __unicode__(self):
        return '%s %s' % (self.vendor.name, self.name)

    def save(self, *args, **kwargs):
        self.note_html = markdown.markdown(self.note)
        super(Phone, self).save(*args, **kwargs)

