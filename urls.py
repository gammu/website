from django.conf.urls import include, url
from django.conf import settings
from news.feeds import RssNewsFeed, AtomNewsFeed
from news.models import Entry
from phonedb.feeds import RssPhonesFeed, AtomPhonesFeed
from phonedb.models import Phone, Vendor
import donate.views
import downloads.views
import phonedb.views
import screenshots.views
import links.views
import news.views
import wammu.views
import tools.views
from django.contrib.sitemaps import GenericSitemap, Sitemap
import django.contrib.sitemaps.views
from django.views.generic import RedirectView
import django.views.static
from downloads.models import Release
import os
import datetime

news_dict = {
    'queryset': Entry.objects.all(),
    'date_field': 'pub_date',
}

phones_dict = {
    'queryset': Phone.objects.all().exclude(state = 'deleted'),
    'date_field': 'created',
}

vendors_dict = {
    'queryset': Vendor.objects.all(),
}

releases_dict = {
    'queryset': Release.objects.all(),
    'date_field': 'date',
}

class PagesSitemap(Sitemap):
    changefreq = 'weekly'

    def items(self):
        return [
            ('/', '%s/index.html' % settings.HTML_ROOT, 1),
            ('/gammu/', '%s/gammu.html' % settings.HTML_ROOT, 1),
            ('/libgammu/', '%s/libgammu.html' % settings.HTML_ROOT, 1),
            ('/wammu/', '%s/wammu.html' % settings.HTML_ROOT, 1),
            ('/smsd/', '%s/smsd.html' % settings.HTML_ROOT, 1),
            ('/python-gammu/', '%s/python-gammu.html' % settings.HTML_ROOT, 1),

            ('/authors/', '%s/authors.html' % settings.HTML_ROOT, 0.9),
            ('/license/', '%s/libgammu.html' % settings.HTML_ROOT, 0.9),
            ('/search/', '%s/search.html' % settings.HTML_ROOT, 0.3),
            ('/donate/', '%s/donate.html' % settings.HTML_ROOT, 0.3),

            ('/s60/', '%s/s60.html' % settings.HTML_ROOT, 0.3),

            ('/support/', '%s/support/index.html' % settings.HTML_ROOT, 0.9),
            ('/support/bugs/', '%s/support/bugs.html' % settings.HTML_ROOT, 0.9),
            ('/support/lists/', '%s/support/lists.html' % settings.HTML_ROOT, 0.9),
            ('/support/online/', '%s/support/online.html' % settings.HTML_ROOT, 0.9),
            ('/support/buy/', '%s/support/buy.html' % settings.HTML_ROOT, 0.9),

            ('/contribute/', '%s/contribute/index.html' % settings.HTML_ROOT, 0.9),
            ('/contribute/code/', '%s/contribute/code.html' % settings.HTML_ROOT, 0.9),
            ('/contribute/translate/', '%s/contribute/translate.html' % settings.HTML_ROOT, 0.9),
            ('/contribute/publicity/', '%s/contribute/publicity.html' % settings.HTML_ROOT, 0.9),
            ('/contribute/wanted/', '%s/contribute/wanted.html' % settings.HTML_ROOT, 0.9),

            ('/docs/', '%s/docs/index.html' % settings.HTML_ROOT, 0.9),

            ('/screenshots/', None, 0.8),
            ('/downloads/gammu/', None, 0.2),
            ('/downloads/gammu/source/', None, 0.7),
            ('/downloads/wammu/', None, 0.2),
            ('/downloads/wammu/source/', None, 0.7),
            ('/links/', None, 0.4),
        ]

    def location(self, item):
        return item[0]

    def lastmod(self, item):
        if item[1] is None:
            return None
        (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(item[1])
        return datetime.datetime.fromtimestamp(mtime)

    def priority(self, item):
        return item[2]

sitemaps = {
    'news': GenericSitemap(news_dict, priority=0.8, changefreq='monthly'),
    'phones': GenericSitemap(phones_dict, priority=0.8, changefreq='monthly'),
    'releases': GenericSitemap(releases_dict, priority=0.9, changefreq='monthly'),
    'vendors': GenericSitemap(vendors_dict, priority=0.2, changefreq='monthly'),
    'pages': PagesSitemap(),
}

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^$', wammu.views.index),
    url(r'^gammu/$', wammu.views.gammu),
    url(r'^smsd/$', wammu.views.smsd),
    url(r'^wammu/$', wammu.views.wammu),
    url(r'^libgammu/$', wammu.views.libgammu),
    url(r'^python-gammu/$', wammu.views.pygammu),

    url(r'^authors/$', wammu.views.static, {'page': 'authors.html'}),
    url(r'^license/$', wammu.views.static, {'page': 'license.html'}),
    url(r'^search/$', wammu.views.static, {'page': 'search.html'}),

    url(r'^support/$', wammu.views.support),
    url(r'^support/bugs/$', wammu.views.static, {'page': 'support/bugs.html'}),
    url(r'^support/lists/$', wammu.views.static, {'page': 'support/lists.html'}),
    url(r'^support/online/$', wammu.views.static, {'page': 'support/online.html'}),
    url(r'^support/buy/$', wammu.views.static, {'page': 'support/buy.html'}),

    url(r'^contribute/$', wammu.views.static, {'page': 'contribute/index.html'}),
    url(r'^contribute/code/$', wammu.views.static, {'page': 'contribute/code.html'}),
    url(r'^contribute/translate/$', wammu.views.static, {'page': 'contribute/translate.html'}),
    url(r'^contribute/publicity/$', wammu.views.static, {'page': 'contribute/publicity.html'}),
    url(r'^contribute/wanted/$', wammu.views.static, {'page': 'contribute/wanted.html'}),

    url(r'^docs/$', wammu.views.static, {'page': 'docs/index.html'}),

    url(r'^s60/$', wammu.views.static, {'page': 's60.html'}),

    url(r'^tools/$', wammu.views.static, {'page': 'tools/index.html'}),
    url(r'^tools/pdu-encode/$', tools.views.pduencode),
    url(r'^tools/pdu-decode/$', tools.views.pdudecode),
    url(r'^tools/countries/$', tools.views.countries),
    url(r'^tools/networks/$', tools.views.networks),

    # RSS feeds
    url(r'^news/rss/$', RssNewsFeed()),
    url(r'^news/atom/$', AtomNewsFeed()),

    # News
    url(r'^news/$', news.views.index),
    url(r'^news/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[^/]*)/$',
        news.views.entry),
    url(r'^news/(?P<slug>[^/]*)/$', news.views.category),

    url(r'^download/$', downloads.views.download),
    url(r'^download/(?P<program>[^/]*)/$', RedirectView.as_view(url='/download/%(program)s/source/', permanent=True)),
    url(r'^download/(?P<program>[^/]*)/(?P<version>[0-9.]*)/$', downloads.views.release),
    url(r'^download/(?P<program>[^/]*)/(?P<platform>[^/]*)/$', downloads.views.list),

    # RSS feeds
    url(r'^phones/rss/$', RssPhonesFeed()),
    url(r'^phones/atom/$', AtomPhonesFeed()),


    url(r'^phones/csv/$', phonedb.views.phones_csv),

    # Phone database
    url(r'^phones/$', phonedb.views.index),
    url(r'^phones/history.png$', phonedb.views.phones_chart),
    url(r'^phones/new/$', phonedb.views.create),
    url(r'^phones/new\.php/$', RedirectView.as_view(url='/phones/new/', permanent=True)),
    url(r'^phones/list\.php', RedirectView.as_view(url='/phones/', permanent=True)),
    url(r'^phones/search/$', phonedb.views.search),
    url(r'^phones/review/$', phonedb.views.review),
    url(r'^phones/model.php/$', phonedb.views.phone_redirect),
    url(r'^phones/search/(?P<featurename>[^/]*)/$', phonedb.views.search),
    url(r'^phones/(?P<vendorname>[^/]*)/$', phonedb.views.vendor),
    url(r'^phones/(?P<vendorname>[^/]*)/(?P<id>[0-9]*)/$', phonedb.views.phone),
    url(r'^phones/(?P<vendorname>[^/]*)/(?P<id>[0-9]*)/delete/$', phonedb.views.delete),
    url(r'^phones/(?P<vendorname>[^/]*)/(?P<id>[0-9]*)/approve/$', phonedb.views.approve),
    url(r'^phones/(?P<vendorname>[^/]*)/new/$', phonedb.views.create),

    # API for Wammu
    url(r'^api/phones/new/$', phonedb.views.create_wammu),

    # DOAP/PAD syndication
    url(r'^api/doap/(?P<program>[^/.]*).xml$', downloads.views.doap),
    url(r'^api/pad/(?P<program>[^/.]*).xml$', downloads.views.pad),
    url(r'^api/pad/padmap.txt$', downloads.views.padmap),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Media files
    url(r'^media/(?P<path>.*)$', django.views.static.serve,
        {'document_root': './media'}),


    # Donations
    url(r'^donate/$', donate.views.donate),
    url(r'^donate/thanks/$', donate.views.thanks),

    # Screenshots
    url(r'^screenshots/$', screenshots.views.index),
    url(r'^screenshots/(?P<slug>[^/]*)/$', screenshots.views.category),

    # Links
    url(r'^links/$', links.views.index),

    # Compatibility
    url(r'^install/$', RedirectView.as_view(url='/download/', permanent=True)),
    url(r'^improve/$', RedirectView.as_view(url='/contribute/', permanent=True)),
    url(r'^wammu.xml$', RedirectView.as_view(url='/api/pad/wammu.xml', permanent=True)),
    url(r'^wammu.doap$', RedirectView.as_view(url='/api/doap/wammu.xml', permanent=True)),
    url(r'^phones/features/(?P<featurename>[^/]*)/$', RedirectView.as_view(url='/phones/search/%(featurename)s/', permanent=True)),

    # Sitemap
    url(r'^sitemap.xml$', django.contrib.sitemaps.views.index, {'sitemaps': sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$', django.contrib.sitemaps.views.sitemap, {'sitemaps': sitemaps}),

    # Robots
    url(r'^robots.txt$', wammu.views.robots),

    # Redirects for crazy bots who investiage full urls
    url(r'^api/$', RedirectView.as_view(url='/download/', permanent=True)),
    url(r'^api/doap/$', RedirectView.as_view(url='/download/', permanent=True)),
    url(r'^api/pad/$', RedirectView.as_view(url='/download/', permanent=True)),

    # Broken links
    url(r'^(?P<link>.*)/\)\.$', RedirectView.as_view(url='/%(link)s', permanent=True)),
    url(r'^(?P<link>.*)/\)$', RedirectView.as_view(url='/%(link)s', permanent=True)),
    url(r'^(?P<link>.*)/index\.php$', RedirectView.as_view(url='/%(link)s', permanent=True)),
    url(r'^(?P<link>phones/(?P<vendorname>[^/]*)/(?P<id>[0-9]*)/),.*', RedirectView.as_view(url='/%(link)s', permanent=True)),
    url(r'^snapshot/$', RedirectView.as_view(url='/download/', permanent=True)),
    url(r'^manual/$', RedirectView.as_view(url='/docs/manual/', permanent=True)),
    url(r'^docs/faq/$', RedirectView.as_view(url='/docs/manual/faq/', permanent=True)),
    url(r'^docs/roadmap/$', RedirectView.as_view(url='/docs/manual/project/roadmap.html', permanent=True)),
    url(r'^docs/devel/$', RedirectView.as_view(url='/docs/', permanent=True)),
    url(r'^docs/man/.*$', RedirectView.as_view(url='/docs/', permanent=True)),
    url(r'^wiki/$', RedirectView.as_view(url='/', permanent=True)),
    url(r'^en/$', RedirectView.as_view(url='http://wammu.eu/', permanent=True)),
    url(r'^cs/$', RedirectView.as_view(url='http://cs.wammu.eu/', permanent=True)),
    url(r'^cz/$', RedirectView.as_view(url='http://cs.wammu.eu/', permanent=True)),
    url(r'^es/$', RedirectView.as_view(url='http://es.wammu.eu/', permanent=True)),
]
