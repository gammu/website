from django.db import models

from django.utils.translation import ugettext_lazy, ugettext as _
from django.core.exceptions import ValidationError

import markdown
import random

# Create your models here.

CONNECTION_CHOICES = (
    ('usb', 'USB'),
    ('serial', 'Serial'),
    ('irda', 'IrDA'),
    ('bluetooth', 'Bluetooth'),
    ('other', 'Other'),
    )

GARBLE_CHOICES = (
    ('atdot', ugettext_lazy('Use [at] and [dot]')),
    ('none', ugettext_lazy('Display it normally')),
    ('hide', ugettext_lazy('Don\'t show email at all')),
    ('nospam', ugettext_lazy('Insert NOSPAM text at random position')),
    )

STATE_CHOICES = (
    ('draft', ugettext_lazy('Draft')),
    ('approved', ugettext_lazy('Approved')),
    ('deleted', ugettext_lazy('Deleted')),
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
    tuxmobil = models.SlugField(null = True, blank = True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
         return ('phonedb.views.vendor', (), {'vendorname': self.slug})

    def get_models_count(self):
        return Phone.objects.filter(vendor = self, state = 'approved').count()

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

def phone_name_validator(value):
    parts = value.split()
    vendor_names = Vendor.objects.all().values_list('name', flat = True)
    vendor_names = [v.lower() for v in vendor_names]
    for part in parts:
        if part.lower() in vendor_names:
            raise ValidationError(_('Phone name should not include vendor name: %s') % part)
    return value

class Phone(models.Model):
    vendor = models.ForeignKey(Vendor)
    name = models.CharField(max_length = 250, help_text = ugettext_lazy('Phone name, please exclude vendor name.'), validators = [phone_name_validator])
    connection = models.ForeignKey(Connection, null = True, blank = True, help_text = ugettext_lazy('Connection used in Gammu configuration.'))
    features = models.ManyToManyField(Feature, help_text = ugettext_lazy('Features which are working in Gammu.'), blank = True)
    model = models.CharField(max_length = 100, blank = True, help_text = ugettext_lazy('Model used in Gammu configuration, usually empty.'))
    gammu_version = models.CharField(max_length = 100, blank = True, help_text = ugettext_lazy('Gammu version where you tested this phone.'))
    note = models.TextField(blank = True, help_text = ugettext_lazy('Any note about this phone and Gammu support for it. You can use <a href="http://daringfireball.net/projects/markdown/syntax">markdown markup</a>.'))
    note_html = models.TextField(editable = False, blank = True)
    author_name = models.CharField(max_length = 250, blank = True)
    author_email = models.EmailField(max_length = 250, blank = True, help_text = ugettext_lazy('Please choose how will be email handled in next field.'))
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
            name = self.name.replace(' ', '_').replace('-', '_')
            if name[:-1] == 'c':
                name = name[:-1] + '_classic'
            result.append({
                'url': 'http://www.forum.nokia.com/Devices/Device_specifications/%s' % name,
                'name': 'Nokia Forum',
            })

        return result

    @models.permalink
    def get_absolute_url(self):
        return ('phonedb.views.phone', (), {'vendorname': self.vendor.slug, 'id': self.id })

    def get_author_email(self):
        if self.author_email == '':
            return None
        elif self.email_garble == 'hide':
            return None
        elif self.email_garble == 'none':
            return self.author_email
        elif self.email_garble == 'atdot':
            return self.author_email.replace('@', '[at]').replace('.', '[dot]')
        else:
            pos = random.randint(0, len(self.author_email))
            return self.author_email[:pos] + 'NOSPAM' + self.author_email[pos:]

    def get_author_name(self):
        if self.email_garble == 'hide':
            return None
        if self.author_name == '':
            return self.get_author_email()
        return self.author_name

    def get_author(self, html = True):
        if self.email_garble == 'hide':
            return None

        mail = self.get_author_email()
        name = self.get_author_name()

        if name is None:
            return None

        if html:
            return '<a href="mailto:%s">%s</a>' % (mail, name)
        else:
            if mail == name:
                return mail
            return '%s (%s)' % (name, mail)
