# -*- coding: UTF-8 -*-
from django.contrib.syndication.views import Feed
from news.models import Entry, Category
from django.utils.feedgenerator import Atom1Feed
from django.utils.translation import ugettext as _
from django.conf import settings

class RssNewsFeed(Feed):
    title = _('Wammu and Gammu News')
    link = '/news/'
    description = _('Updates about Wammu and Gammu programs.')
    copyright = 'Copyright © 2003 - 2012 Michal Čihař'
    item_copyright = copyright
    title_template ='feeds/news_title.html'
    description_template = 'feeds/news_description.html'

    def categories(self):
        print [x.title for x in Category.objects.all()]

    def items(self):
        return Entry.objects.order_by('-pub_date')[:settings.NEWS_IN_RSS]

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

