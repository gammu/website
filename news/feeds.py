# -*- coding: UTF-8 -*-
from django.contrib.syndication.feeds import Feed
from news.models import Entry, Category
from django.utils.feedgenerator import Atom1Feed

class RssNewsFeed(Feed):
    title = 'Wammu and Gammu News'
    link = '/news/'
    description = 'Updates about Wammu and Gammu programs.'
    copyright = 'Copyright © 2003 - 2009 Michal Čihař'

    def categories(self):
        print [x.title for x in Category.objects.all()]

    def items(self):
        return Entry.objects.order_by('-pub_date')[:5]

    def item_author_name(self, obj):
        return obj.author.get_full_name()

    def item_author_email(self, obj):
        return obj.author.email

    def item_categories(self, obj):
        return [x.title for x in obj.categories.get_query_set()]


class AtomNewsFeed(RssNewsFeed):
    feed_type = Atom1Feed
    subtitle = RssNewsFeed.description

