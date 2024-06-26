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
            ("/", f"{settings.HTML_ROOT}/index.html", 1),
            ("/gammu/", f"{settings.HTML_ROOT}/gammu.html", 1),
            ("/libgammu/", f"{settings.HTML_ROOT}/libgammu.html", 1),
            ("/wammu/", f"{settings.HTML_ROOT}/wammu.html", 1),
            ("/smsd/", f"{settings.HTML_ROOT}/smsd.html", 1),
            ("/python-gammu/", f"{settings.HTML_ROOT}/python-gammu.html", 1),
            ("/authors/", f"{settings.HTML_ROOT}/authors.html", 0.9),
            ("/license/", f"{settings.HTML_ROOT}/libgammu.html", 0.9),
            ("/donate/", f"{settings.HTML_ROOT}/donate.html", 0.3),
            ("/s60/", f"{settings.HTML_ROOT}/s60.html", 0.3),
            ("/support/", f"{settings.HTML_ROOT}/support/index.html", 0.9),
            ("/support/bugs/", f"{settings.HTML_ROOT}/support/bugs.html", 0.9),
            ("/support/lists/", f"{settings.HTML_ROOT}/support/lists.html", 0.9),
            ("/support/online/", f"{settings.HTML_ROOT}/support/online.html", 0.9),
            ("/support/buy/", f"{settings.HTML_ROOT}/support/buy.html", 0.9),
            ("/contribute/", f"{settings.HTML_ROOT}/contribute/index.html", 0.9),
            ("/contribute/code/", f"{settings.HTML_ROOT}/contribute/code.html", 0.9),
            (
                "/contribute/translate/",
                f"{settings.HTML_ROOT}/contribute/translate.html",
                0.9,
            ),
            (
                "/contribute/publicity/",
                f"{settings.HTML_ROOT}/contribute/publicity.html",
                0.9,
            ),
            (
                "/contribute/wanted/",
                f"{settings.HTML_ROOT}/contribute/wanted.html",
                0.9,
            ),
            ("/docs/", f"{settings.HTML_ROOT}/docs/index.html", 0.9),
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
    path("", wammu.views.index, name="home"),
    path("gammu/", wammu.views.gammu, name="gammu"),
    path("smsd/", wammu.views.smsd, name="smsd"),
    path("wammu/", wammu.views.wammu, name="wammu"),
    path("libgammu/", wammu.views.libgammu, name="libgammu"),
    path("python-gammu/", wammu.views.pygammu, name="python-gammu"),
    path("authors/", wammu.views.static, {"page": "authors.html"}, name="authors"),
    path("license/", wammu.views.static, {"page": "license.html"}, name="license"),
    path("search/", RedirectView.as_view(url="/", permanent=True)),
    path("support/", wammu.views.support, name="support"),
    path("support/bugs/", wammu.views.static, {"page": "support/bugs.html"}),
    path("support/lists/", wammu.views.static, {"page": "support/lists.html"}),
    path("support/online/", wammu.views.static, {"page": "support/online.html"}),
    path("support/buy/", wammu.views.static, {"page": "support/buy.html"}),
    path("contribute/", wammu.views.static, {"page": "contribute/index.html"}),
    path("contribute/code/", wammu.views.static, {"page": "contribute/code.html"}),
    path(
        "contribute/translate/",
        wammu.views.static,
        {"page": "contribute/translate.html"},
    ),
    path(
        "contribute/publicity/",
        wammu.views.static,
        {"page": "contribute/publicity.html"},
    ),
    path("contribute/wanted/", wammu.views.static, {"page": "contribute/wanted.html"}),
    path("docs/", wammu.views.static, {"page": "docs/index.html"}),
    path("s60/", wammu.views.static, {"page": "s60.html"}),
    path("tools/", wammu.views.static, {"page": "tools/index.html"}),
    path("tools/pdu-encode/", tools.views.pduencode, name="pduencode"),
    path("tools/pdu-decode/", tools.views.pdudecode, name="pdudecode"),
    path("tools/countries/", tools.views.countries, name="countries"),
    path("tools/networks/", tools.views.networks, name="networks"),
    # RSS feeds
    path("news/rss/", RssNewsFeed()),
    path("news/atom/", AtomNewsFeed()),
    # News
    path("news/", news.views.index, name="news"),
    re_path(
        r"^news/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[^/]+)/$",
        news.views.entry,
        name="news-entry",
    ),
    path("news/<str:slug>/", news.views.category, name="news-category"),
    path(
        "download/",
        downloads.views.download,
        name="downloads",
    ),
    path(
        "download/<str:program>/",
        downloads.views.detail,
        name="downloads-detail",
    ),
    re_path(
        r"^download/(?P<program>[^/]+)/(?P<version>[0-9.]+)/$",
        downloads.views.release,
        name="downloads-release",
    ),
    path(
        "download/<str:program>/<str:platform>/",
        RedirectView.as_view(url="/download/%(program)s/", permanent=True),
    ),
    # RSS feeds
    path("phones/rss/", RssPhonesFeed(), name="phonedb-rss"),
    path("phones/atom/", AtomPhonesFeed()),
    path("phones/csv/", phonedb.views.phones_csv, name="phonedb-csv"),
    # Phone database
    path("phones/", phonedb.views.index, name="phonedb"),
    re_path(r"^phones/history.png$", phonedb.views.phones_chart),
    path("phones/new/", phonedb.views.create, name="phonedb-new"),
    re_path(
        r"^phones/new\.php/$",
        RedirectView.as_view(url="/phones/new/", permanent=True),
    ),
    re_path(r"^phones/list\.php", RedirectView.as_view(url="/phones/", permanent=True)),
    path("phones/search/", phonedb.views.search, name="phonedb-search"),
    path("phones/review/", phonedb.views.review),
    re_path(r"^phones/model.php/$", phonedb.views.phone_redirect),
    path(
        "phones/search/<str:featurename>/",
        phonedb.views.search,
        name="phonedb-search-feature",
    ),
    path("phones/<str:vendorname>/", phonedb.views.vendor, name="phonedb-vendor"),
    path(
        "phones/<str:vendorname>/<int:pk>/",
        phonedb.views.phone,
        name="phonedb-phone",
    ),
    path("phones/<str:vendorname>/<int:pk>/delete/", phonedb.views.delete),
    path("phones/<str:vendorname>/<int:pk>/approve/", phonedb.views.approve),
    path("phones/<str:vendorname>/new/", phonedb.views.create),
    # API for Wammu
    path("api/phones/new/", phonedb.views.create_wammu, name="phonedb-api"),
    # DOAP/PAD syndication
    re_path(r"^api/doap/(?P<program>[^/.]+).xml$", downloads.views.doap),
    re_path(r"^api/pad/(?P<program>[^/.]+).xml$", downloads.views.pad),
    re_path(r"^api/pad/padmap.txt$", downloads.views.padmap),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    path("admin/", admin.site.urls),
    # Media files
    re_path(
        r"^media/(?P<path>.*)$",
        django.views.static.serve,
        {"document_root": "./media"},
    ),
    # Donations
    path("donate/", donate.views.donate),
    path("donate/thanks/", donate.views.thanks),
    # Screenshots
    path("screenshots/", screenshots.views.index),
    path(
        "screenshots/<str:slug>/",
        screenshots.views.category,
        name="screenshots-category",
    ),
    # Links
    path("links/", links.views.index),
    # Compatibility
    path("install/", RedirectView.as_view(url="/download/", permanent=True)),
    path("improve/", RedirectView.as_view(url="/contribute/", permanent=True)),
    re_path(
        r"^wammu.xml$",
        RedirectView.as_view(url="/api/pad/wammu.xml", permanent=True),
    ),
    re_path(
        r"^wammu.doap$",
        RedirectView.as_view(url="/api/doap/wammu.xml", permanent=True),
    ),
    path(
        "phones/features/<str:featurename>/",
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
    path("api/", RedirectView.as_view(url="/download/", permanent=True)),
    path("api/doap/", RedirectView.as_view(url="/download/", permanent=True)),
    path("api/pad/", RedirectView.as_view(url="/download/", permanent=True)),
    # Broken links
    re_path(
        r"^(?P<link>.*)/\)\.$",
        RedirectView.as_view(url="/%(link)s", permanent=True),
    ),
    re_path(
        r"^(?P<link>.*)/\)$",
        RedirectView.as_view(url="/%(link)s", permanent=True),
    ),
    re_path(
        r"^(?P<link>.*)/index\.php$",
        RedirectView.as_view(url="/%(link)s", permanent=True),
    ),
    re_path(
        r"^(?P<link>phones/(?P<vendorname>[^/]+)/(?P<pk>[0-9]+)/),.*",
        RedirectView.as_view(url="/%(link)s", permanent=True),
    ),
    path("snapshot/", RedirectView.as_view(url="/download/", permanent=True)),
    path(
        "manual/",
        RedirectView.as_view(url="https://docs.gammu.org/", permanent=True),
    ),
    path(
        "docs/faq/",
        RedirectView.as_view(url="https://docs.gammu.org/faq/", permanent=True),
    ),
    path(
        "docs/roadmap/",
        RedirectView.as_view(
            url="https://docs.gammu.org/project/roadmap.html",
            permanent=True,
        ),
    ),
    path("docs/devel/", RedirectView.as_view(url="/docs/", permanent=True)),
    re_path(r"^docs/man/.*$", RedirectView.as_view(url="/docs/", permanent=True)),
    path("wiki/", RedirectView.as_view(url="/", permanent=True)),
    path("en/", RedirectView.as_view(url="https://wammu.eu/", permanent=True)),
    path("cs/", RedirectView.as_view(url="https://cs.wammu.eu/", permanent=True)),
    path("cz/", RedirectView.as_view(url="https://cs.wammu.eu/", permanent=True)),
    path("es/", RedirectView.as_view(url="https://es.wammu.eu/", permanent=True)),
]
if settings.DEBUG and "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
