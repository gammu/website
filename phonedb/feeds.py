# -*- coding: UTF-8 -*-
from django.contrib.syndication.feeds import Feed
from phonedb.models import Vendor, Phone
from django.utils.feedgenerator import Atom1Feed
from django.utils.translation import ugettext as _
from django.conf import settings

class RssPhonesFeed(Feed):
    title = _('Gammu Phone Database')
    link = '/phones/'
    description = _('Gammu phone database updates.')
    copyright = 'Copyright © 2003 - 2009 Michal Čihař'
    item_copyright = copyright

    def categories(self):
        print [x.name for x in Vendor.objects.all()]

    def items(self):
        return Phone.objects.filter(state__in = ['approved', 'draft']).order_by('-created')[:settings.PHONES_IN_RSS]

    def item_author_name(self, obj):
        return obj.get_author_name()

    def item_author_email(self, obj):
        return obj.get_author_email()

    def item_categories(self, obj):
        return [obj.vendor.name]

    def item_pubdate(self, obj):
        return obj.created

class AtomPhonesFeed(RssPhonesFeed):
    feed_type = Atom1Feed
    subtitle = RssPhonesFeed.description


