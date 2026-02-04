from django.conf import settings
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.utils.translation import gettext as _

from news.models import Entry


class RssNewsFeed(Feed):
    link = "/news/"
    copyright = "Copyright © Michal Čihař"
    item_copyright = copyright  # noqa: A003
    title_template = "feeds/news_title.html"
    description_template = "feeds/news_description.html"

    def title(self):
        return _("Wammu and Gammu News")

    def description(self):
        return _("Updates about Wammu and Gammu programs.")

    def items(self):
        return Entry.objects.order_by("-pub_date")[: settings.NEWS_IN_RSS]

    def item_author_name(self, obj):
        return obj.author.get_full_name()

    def item_author_email(self, obj):
        return obj.author.email

    def item_categories(self, obj):
        return [x.title for x in obj.categories.all()]

    def item_pubdate(self, obj):
        return obj.pub_date


class AtomNewsFeed(RssNewsFeed):
    feed_type = Atom1Feed
    subtitle = RssNewsFeed.description
