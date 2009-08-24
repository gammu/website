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

    (r'^news/$', 'news.views.index'),
    (r'^news/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[^/]*)/$',
        'news.views.entry'),

    (r'^download/(?P<program>[^/]*)/(?P<platform>[^/]*)/$', 'downloads.views.list'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    # Media files
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': './media'}),

    # RSS feeds
    (r'^news/(?P<url>[a-z].*)/$', 'django.contrib.syndication.views.feed',
        {'feed_dict': feeds}),
)
