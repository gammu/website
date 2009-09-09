from django.db import models

from django.utils.translation import ugettext_lazy

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

FEATURE_NAMES = {
    'info': ugettext_lazy('Phone information'),
    'sms': ugettext_lazy('Sending and saving SMS'),
    'mms': ugettext_lazy('Multimedia messaging'),
    'phonebook': ugettext_lazy('Basic phonebook functions (name and phone number)'),
    'enhancedphonebook': ugettext_lazy('Enhanced phonebook entries (eg. several numbers per entry)'),
    'calendar': ugettext_lazy('Calendar entries'),
    'todo': ugettext_lazy('Todos'),
    'filesystem': ugettext_lazy('Filesystem manipulation'),
    'call': ugettext_lazy('Reading and making calls'),
    'logo': ugettext_lazy('Logos'),
    'ringtone': ugettext_lazy('Ringtones'),
}

class Vendor(models.Model):
    name = models.CharField(max_length = 250)
    url = models.URLField(max_length = 250)
    slug = models.SlugField(unique = True)
    tuxmobil = models.SlugField(null = True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
         return ('phonedb.views.vendor', (), {'vendorname': self.slug})

class Feature(models.Model):
    name = models.CharField(max_length = 250)

    def __unicode__(self):
        return self.name

    def get_description(self):
        return FEATURE_NAMES[self.name]

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

    def get_related_sites(self):
        result = []
        name = self.__unicode__().replace(' ', '_').replace('-', '_')
        result.append({
            'url': 'http://wikipedia.org/wiki/%s' % name,
            'name': 'Wikipedia',
        })
        name = self.name.replace(' ', '_').replace('-', '_')
        vendor = self.vendor.name.replace('-', '_').replace(' ', '_')
        result.append({
            'url': 'http://www.mobile-phone-directory.org/Phones/%s/%s_%s.html' % (vendor, vendor, name),
            'name': 'The Mobile Phone Directory',
        })
        name = self.name.replace(' ', '').replace('-', '').lower()
        vendor = self.vendor.slug.replace('-', '_').replace(' ', '_')
        result.append({
            'url': 'http://www.mobiledia.com/phones/%s/%s.html' % (vendor, name),
            'name': 'Mobilemedia',
        })
        if self.vendor.slug == 'nokia':
            name = self.name.replace(' ', '_').replace('-', '_').upper()
            result.append({
                'url': 'http://www.forum.nokia.com/devices/%s' % name,
                'name': 'Nokia Forum',
            })

        return result

    @models.permalink
    def get_absolute_url(self):
         return ('phonedb.views.phone', (), {'vendorname': self.vendor.slug, 'id': self.id })
