"""Tests for sitemaps."""

from xml.etree import ElementTree as ET

from django.contrib.sites.models import Site
from django.test import TestCase

from news.models import Category


class SitemapTest(TestCase):
    def setUp(self):
        Site.objects.create(domain="testserver")

    def test_sitemaps(self):
        # Get root sitemap
        response = self.client.get("/sitemap.xml")
        self.assertContains(response, "<sitemapindex")

        # Parse it
        tree = ET.fromstring(response.content)
        sitemaps = tree.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap")
        for sitemap in sitemaps:
            location = sitemap.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
            response = self.client.get(location.text)
            self.assertContains(response, "<urlset")
            # Try if it's a valid XML
            ET.fromstring(response.content)

    def test_support_sitemap_uses_community_page(self):
        response = self.client.get("/sitemap-pages.xml")

        self.assertContains(response, "/support/community/")
        self.assertNotContains(response, "/support/lists/")
        self.assertNotContains(response, "/support/online/")


class SupportPagesTest(TestCase):
    def test_community_page(self):
        response = self.client.get("/support/community/")

        self.assertContains(
            response,
            "https://github.com/gammu/gammu/discussions",
        )
        self.assertContains(response, "/support/bugs/")
        self.assertContains(response, "/support/buy/")

    def test_pages_do_not_advertise_retired_channels(self):
        for page_url in (
            "/support/",
            "/support/community/",
            "/support/buy/",
            "/docs/",
            "/contribute/code/",
            "/contribute/wanted/",
            "/tools/",
        ):
            with self.subTest(page_url=page_url):
                rendered = self.client.get(page_url).content.decode().lower()
                for retired_channel in (
                    "mailing list",
                    "irc",
                    "jabber",
                    "freenode",
                    "sourceforge",
                    "stack overflow",
                    "/support/lists/",
                    "/support/online/",
                ):
                    self.assertNotIn(retired_channel, rendered)

    def test_legacy_community_urls_redirect_permanently(self):
        for legacy_url in ("/support/lists/", "/support/online/"):
            with self.subTest(legacy_url=legacy_url):
                self.assertRedirects(
                    self.client.get(legacy_url),
                    "/support/community/",
                    status_code=301,
                    fetch_redirect_response=False,
                )

    def test_private_vulnerability_reporting(self):
        response = self.client.get("/support/bugs/")

        self.assertContains(
            response,
            "https://github.com/gammu/gammu/security/advisories/new",
        )
        self.assertContains(
            response,
            "https://github.com/gammu/python-gammu/security/advisories/new",
        )
        self.assertContains(
            response,
            "Do not disclose security vulnerabilities in a public issue",
        )


class FrontendTest(TestCase):
    def test_first_party_frontend(self):
        response = self.client.get("/")

        self.assertContains(response, "/static/css/own.css")
        self.assertContains(response, "/static/js/init.js")
        self.assertContains(response, "/static/images/icons.svg")
        self.assertContains(response, "data-lightbox-dialog")
        self.assertContains(response, "data-menu", count=9)
        self.assertContains(response, '<article class="product-card', count=5)
        self.assertNotContains(response, "Not currently maintained")
        self.assertNotContains(response, "View details")

        for removed_integration in (
            "bootstrap",
            "crispy",
            "jquery",
            "colorbox",
            "font-awesome",
            "piwik",
            "piwik_download",
            "_paq",
            "stats.cihar.com",
        ):
            self.assertNotContains(response, removed_integration)

    def test_wammu_maintenance_status(self):
        Category.objects.create(
            title="Wammu",
            slug="wammu",
            description="Wammu news",
        )
        response = self.client.get("/wammu/")

        self.assertContains(response, "Wammu is not currently maintained.")
        self.assertContains(response, "current Python versions")
        self.assertContains(response, "current python-gammu")
        self.assertContains(response, "News archive")
        self.assertContains(response, "issues are not actively triaged")
