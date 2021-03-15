from django.conf import settings
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.utils.translation import ugettext as _

from phonedb.models import Phone, Vendor


class RssPhonesFeed(Feed):
    link = "/phones/"
    copyright = "Copyright © 2003 - 2021 Michal Čihař"
    item_copyright = copyright
    title_template = "feeds/phones_title.html"
    description_template = "feeds/phones_description.html"

    def title(self):
        return _("Gammu Phone Database")

    def description(self):
        return _("Gammu phone database updates.")

    def categories(self):
        return [x.name for x in Vendor.objects.all()]

    def items(self):
        return Phone.objects.exclude(state="deleted").order_by("-created")[
            : settings.PHONES_IN_RSS
        ]

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
