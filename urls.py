from django.conf.urls.defaults import *
from news.feeds import RssNewsFeed, AtomNewsFeed

feeds = {
    'rss': RssNewsFeed,
    'atom': AtomNewsFeed,
}

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^wammu/', include('wammu.foo.urls')),
    (r'^$', 'wammu.views.index'),
    (r'^gammu/$', 'wammu.views.gammu'),
    (r'^smsd/$', 'wammu.views.smsd'),
    (r'^wammu/$', 'wammu.views.wammu'),
    (r'^libgammu/$', 'wammu.views.libgammu'),
    (r'^python-gammu/$', 'wammu.views.pygammu'),

    (r'^authors/$', 'wammu.views.static', {'page': 'authors.html'}),
    (r'^license/$', 'wammu.views.static', {'page': 'license.html'}),

    (r'^support/$', 'wammu.views.static', {'page': 'support/index.html'}),
    (r'^support/bugs/$', 'wammu.views.static', {'page': 'support/bugs.html'}),
    (r'^support/lists/$', 'wammu.views.static', {'page': 'support/lists.html'}),
    (r'^support/online/$', 'wammu.views.static', {'page': 'support/online.html'}),
    (r'^support/buy/$', 'wammu.views.static', {'page': 'support/buy.html'}),

    # RSS feeds
    (r'^news/(?P<url>(rss|atom).*)/$', 'django.contrib.syndication.views.feed',
        {'feed_dict': feeds}),

    # News
    (r'^news/$', 'news.views.index'),
    (r'^news/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[^/]*)/$',
        'news.views.entry'),
    (r'^news/(?P<slug>.*)/$', 'news.views.category'),

    (r'^download/(?P<program>[^/]*)/(?P<version>[0-9.]*)/$', 'downloads.views.release'),
    (r'^download/(?P<program>[^/]*)/(?P<platform>[^/]*)/$', 'downloads.views.list'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    # Media files
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': './media'}),


    # Donations
    (r'^donate/$', 'donate.views.donate'),
    (r'^donate/done/', include('paypal.standard.pdt.urls')),

    # Screenshots
    (r'^screenshots/$', 'screenshots.views.index'),
    (r'^screenshots/(?P<slug>.*)/$', 'screenshots.views.category'),

    # Links
    (r'^links/$', 'links.views.index'),
)
