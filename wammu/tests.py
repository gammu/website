"""Tests for sitemaps."""

from xml.etree import ElementTree as ET

from django.contrib.sites.models import Site
from django.test import TestCase


class SitemapTest(TestCase):
    def test_sitemaps(self):
        Site.objects.create(domain="testserver")
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


class FrontendTest(TestCase):
    def test_first_party_frontend(self):
        response = self.client.get("/")

        self.assertContains(response, "/static/css/own.css")
        self.assertContains(response, "/static/js/init.js")
        self.assertContains(response, "/static/images/icons.svg")
        self.assertContains(response, "data-lightbox-dialog")
        self.assertContains(response, "data-menu", count=9)

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
