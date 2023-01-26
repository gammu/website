import datetime
import os

import django.contrib.sitemaps.views
import django.views.static
from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps import GenericSitemap, Sitemap
from django.urls import include, path, re_path
from django.views.generic import RedirectView

import donate.views
import downloads.views
import links.views
import news.views
import phonedb.views
import screenshots.views
import tools.views
import wammu.views
from downloads.models import Release
from news.feeds import AtomNewsFeed, RssNewsFeed
from news.models import Entry
from phonedb.feeds import AtomPhonesFeed, RssPhonesFeed
from phonedb.models import Phone, Vendor

news_dict = {
    "queryset": Entry.objects.all(),
    "date_field": "pub_date",
}

phones_dict = {
    "queryset": Phone.objects.exclude(state="deleted").prefetch_related("vendor"),
    "date_field": "created",
}

vendors_dict = {
    "queryset": Vendor.objects.all(),
}

releases_dict = {
    "queryset": Release.objects.all(),
    "date_field": "date",
}


class PagesSitemap(Sitemap):
    changefreq = "weekly"

    def items(self):
        return [
            ("/", "%s/index.html" % settings.HTML_ROOT, 1),
            ("/gammu/", "%s/gammu.html" % settings.HTML_ROOT, 1),
            ("/libgammu/", "%s/libgammu.html" % settings.HTML_ROOT, 1),
            ("/wammu/", "%s/wammu.html" % settings.HTML_ROOT, 1),
            ("/smsd/", "%s/smsd.html" % settings.HTML_ROOT, 1),
            ("/python-gammu/", "%s/python-gammu.html" % settings.HTML_ROOT, 1),
            ("/authors/", "%s/authors.html" % settings.HTML_ROOT, 0.9),
            ("/license/", "%s/libgammu.html" % settings.HTML_ROOT, 0.9),
            ("/donate/", "%s/donate.html" % settings.HTML_ROOT, 0.3),
            ("/s60/", "%s/s60.html" % settings.HTML_ROOT, 0.3),
            ("/support/", "%s/support/index.html" % settings.HTML_ROOT, 0.9),
            ("/support/bugs/", "%s/support/bugs.html" % settings.HTML_ROOT, 0.9),
            ("/support/lists/", "%s/support/lists.html" % settings.HTML_ROOT, 0.9),
            ("/support/online/", "%s/support/online.html" % settings.HTML_ROOT, 0.9),
            ("/support/buy/", "%s/support/buy.html" % settings.HTML_ROOT, 0.9),
            ("/contribute/", "%s/contribute/index.html" % settings.HTML_ROOT, 0.9),
            ("/contribute/code/", "%s/contribute/code.html" % settings.HTML_ROOT, 0.9),
            (
                "/contribute/translate/",
                "%s/contribute/translate.html" % settings.HTML_ROOT,
                0.9,
            ),
            (
                "/contribute/publicity/",
                "%s/contribute/publicity.html" % settings.HTML_ROOT,
                0.9,
            ),
            (
                "/contribute/wanted/",
                "%s/contribute/wanted.html" % settings.HTML_ROOT,
                0.9,
            ),
            ("/docs/", "%s/docs/index.html" % settings.HTML_ROOT, 0.9),
            ("/screenshots/", None, 0.8),
            ("/downloads/gammu/", None, 0.7),
            ("/downloads/python-gammu/", None, 0.7),
            ("/downloads/wammu/", None, 0.7),
            ("/links/", None, 0.4),
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
    "news": GenericSitemap(news_dict, priority=0.8, changefreq="monthly"),
    "phones": GenericSitemap(phones_dict, priority=0.8, changefreq="monthly"),
    "releases": GenericSitemap(releases_dict, priority=0.9, changefreq="monthly"),
    "vendors": GenericSitemap(vendors_dict, priority=0.2, changefreq="monthly"),
    "pages": PagesSitemap(),
}

admin.autodiscover()

urlpatterns = [
    re_path(r"^$", wammu.views.index, name="home"),
    re_path(r"^gammu/$", wammu.views.gammu, name="gammu"),
    re_path(r"^smsd/$", wammu.views.smsd, name="smsd"),
    re_path(r"^wammu/$", wammu.views.wammu, name="wammu"),
    re_path(r"^libgammu/$", wammu.views.libgammu, name="libgammu"),
    re_path(r"^python-gammu/$", wammu.views.pygammu, name="python-gammu"),
    re_path(
        r"^authors/$", wammu.views.static, {"page": "authors.html"}, name="authors"
    ),
    re_path(
        r"^license/$", wammu.views.static, {"page": "license.html"}, name="license"
    ),
    re_path(r"^search/$", RedirectView.as_view(url="/", permanent=True)),
    re_path(r"^support/$", wammu.views.support, name="support"),
    re_path(r"^support/bugs/$", wammu.views.static, {"page": "support/bugs.html"}),
    re_path(r"^support/lists/$", wammu.views.static, {"page": "support/lists.html"}),
    re_path(r"^support/online/$", wammu.views.static, {"page": "support/online.html"}),
    re_path(r"^support/buy/$", wammu.views.static, {"page": "support/buy.html"}),
    re_path(r"^contribute/$", wammu.views.static, {"page": "contribute/index.html"}),
    re_path(
        r"^contribute/code/$", wammu.views.static, {"page": "contribute/code.html"}
    ),
    re_path(
        r"^contribute/translate/$",
        wammu.views.static,
        {"page": "contribute/translate.html"},
    ),
    re_path(
        r"^contribute/publicity/$",
        wammu.views.static,
        {"page": "contribute/publicity.html"},
    ),
    re_path(
        r"^contribute/wanted/$", wammu.views.static, {"page": "contribute/wanted.html"}
    ),
    re_path(r"^docs/$", wammu.views.static, {"page": "docs/index.html"}),
    re_path(r"^s60/$", wammu.views.static, {"page": "s60.html"}),
    re_path(r"^tools/$", wammu.views.static, {"page": "tools/index.html"}),
    re_path(r"^tools/pdu-encode/$", tools.views.pduencode, name="pduencode"),
    re_path(r"^tools/pdu-decode/$", tools.views.pdudecode, name="pdudecode"),
    re_path(r"^tools/countries/$", tools.views.countries, name="countries"),
    re_path(r"^tools/networks/$", tools.views.networks, name="networks"),
    # RSS feeds
    re_path(r"^news/rss/$", RssNewsFeed()),
    re_path(r"^news/atom/$", AtomNewsFeed()),
    # News
    re_path(r"^news/$", news.views.index, name="news"),
    re_path(
        r"^news/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[^/]+)/$",
        news.views.entry,
        name="news-entry",
    ),
    re_path(r"^news/(?P<slug>[^/]+)/$", news.views.category, name="news-category"),
    re_path(
        r"^download/$",
        downloads.views.download,
        name="downloads",
    ),
    re_path(
        r"^download/(?P<program>[^/]+)/$",
        downloads.views.detail,
        name="downloads-detail",
    ),
    re_path(
        r"^download/(?P<program>[^/]+)/(?P<version>[0-9.]+)/$",
        downloads.views.release,
        name="downloads-release",
    ),
    re_path(
        r"^download/(?P<program>[^/]+)/(?P<platform>[^/]+)/$",
        RedirectView.as_view(url="/download/%(program)s/", permanent=True),
    ),
    # RSS feeds
    re_path(r"^phones/rss/$", RssPhonesFeed(), name="phonedb-rss"),
    re_path(r"^phones/atom/$", AtomPhonesFeed()),
    re_path(r"^phones/csv/$", phonedb.views.phones_csv, name="phonedb-csv"),
    # Phone database
    re_path(r"^phones/$", phonedb.views.index, name="phonedb"),
    re_path(r"^phones/history.png$", phonedb.views.phones_chart),
    re_path(r"^phones/new/$", phonedb.views.create, name="phonedb-new"),
    re_path(
        r"^phones/new\.php/$", RedirectView.as_view(url="/phones/new/", permanent=True)
    ),
    re_path(r"^phones/list\.php", RedirectView.as_view(url="/phones/", permanent=True)),
    re_path(r"^phones/search/$", phonedb.views.search, name="phonedb-search"),
    re_path(r"^phones/review/$", phonedb.views.review),
    re_path(r"^phones/model.php/$", phonedb.views.phone_redirect),
    re_path(
        r"^phones/search/(?P<featurename>[^/]+)/$",
        phonedb.views.search,
        name="phonedb-search-feature",
    ),
    re_path(
        r"^phones/(?P<vendorname>[^/]+)/$", phonedb.views.vendor, name="phonedb-vendor"
    ),
    re_path(
        r"^phones/(?P<vendorname>[^/]+)/(?P<id>[0-9]+)/$",
        phonedb.views.phone,
        name="phonedb-phone",
    ),
    re_path(
        r"^phones/(?P<vendorname>[^/]+)/(?P<id>[0-9]+)/delete/$", phonedb.views.delete
    ),
    re_path(
        r"^phones/(?P<vendorname>[^/]+)/(?P<id>[0-9]+)/approve/$", phonedb.views.approve
    ),
    re_path(r"^phones/(?P<vendorname>[^/]+)/new/$", phonedb.views.create),
    # API for Wammu
    re_path(r"^api/phones/new/$", phonedb.views.create_wammu, name="phonedb-api"),
    # DOAP/PAD syndication
    re_path(r"^api/doap/(?P<program>[^/.]+).xml$", downloads.views.doap),
    re_path(r"^api/pad/(?P<program>[^/.]+).xml$", downloads.views.pad),
    re_path(r"^api/pad/padmap.txt$", downloads.views.padmap),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    path("admin/", admin.site.urls),
    # Media files
    re_path(
        r"^media/(?P<path>.*)$", django.views.static.serve, {"document_root": "./media"}
    ),
    # Donations
    re_path(r"^donate/$", donate.views.donate),
    re_path(r"^donate/thanks/$", donate.views.thanks),
    # Screenshots
    re_path(r"^screenshots/$", screenshots.views.index),
    re_path(
        r"^screenshots/(?P<slug>[^/]+)/$",
        screenshots.views.category,
        name="screenshots-category",
    ),
    # Links
    re_path(r"^links/$", links.views.index),
    # Compatibility
    re_path(r"^install/$", RedirectView.as_view(url="/download/", permanent=True)),
    re_path(r"^improve/$", RedirectView.as_view(url="/contribute/", permanent=True)),
    re_path(
        r"^wammu.xml$", RedirectView.as_view(url="/api/pad/wammu.xml", permanent=True)
    ),
    re_path(
        r"^wammu.doap$", RedirectView.as_view(url="/api/doap/wammu.xml", permanent=True)
    ),
    re_path(
        r"^phones/features/(?P<featurename>[^/]+)/$",
        RedirectView.as_view(url="/phones/search/%(featurename)s/", permanent=True),
    ),
    # Sitemap
    re_path(
        r"^sitemap.xml$",
        django.contrib.sitemaps.views.index,
        {"sitemaps": sitemaps},
        name="sitemap",
    ),
    re_path(
        r"^sitemap-(?P<section>.+)\.xml$",
        django.contrib.sitemaps.views.sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    # Robots
    re_path(r"^robots.txt$", wammu.views.robots),
    # Redirects for crazy bots who investiage full urls
    re_path(r"^api/$", RedirectView.as_view(url="/download/", permanent=True)),
    re_path(r"^api/doap/$", RedirectView.as_view(url="/download/", permanent=True)),
    re_path(r"^api/pad/$", RedirectView.as_view(url="/download/", permanent=True)),
    # Broken links
    re_path(
        r"^(?P<link>.*)/\)\.$", RedirectView.as_view(url="/%(link)s", permanent=True)
    ),
    re_path(
        r"^(?P<link>.*)/\)$", RedirectView.as_view(url="/%(link)s", permanent=True)
    ),
    re_path(
        r"^(?P<link>.*)/index\.php$",
        RedirectView.as_view(url="/%(link)s", permanent=True),
    ),
    re_path(
        r"^(?P<link>phones/(?P<vendorname>[^/]+)/(?P<id>[0-9]+)/),.*",
        RedirectView.as_view(url="/%(link)s", permanent=True),
    ),
    re_path(r"^snapshot/$", RedirectView.as_view(url="/download/", permanent=True)),
    re_path(
        r"^manual/$",
        RedirectView.as_view(url="https://docs.gammu.org/", permanent=True),
    ),
    re_path(
        r"^docs/faq/$",
        RedirectView.as_view(url="https://docs.gammu.org/faq/", permanent=True),
    ),
    re_path(
        r"^docs/roadmap/$",
        RedirectView.as_view(
            url="https://docs.gammu.org/project/roadmap.html", permanent=True
        ),
    ),
    re_path(r"^docs/devel/$", RedirectView.as_view(url="/docs/", permanent=True)),
    re_path(r"^docs/man/.*$", RedirectView.as_view(url="/docs/", permanent=True)),
    re_path(r"^wiki/$", RedirectView.as_view(url="/", permanent=True)),
    re_path(r"^en/$", RedirectView.as_view(url="https://wammu.eu/", permanent=True)),
    re_path(r"^cs/$", RedirectView.as_view(url="https://cs.wammu.eu/", permanent=True)),
    re_path(r"^cz/$", RedirectView.as_view(url="https://cs.wammu.eu/", permanent=True)),
    re_path(r"^es/$", RedirectView.as_view(url="https://es.wammu.eu/", permanent=True)),
]
if settings.DEBUG and "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
