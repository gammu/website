import datetime
import xml.etree.ElementTree as ET
from unittest import mock

from django.contrib.sites.models import Site
from django.core.cache import cache
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from django.utils import translation

from phonedb.charts import get_phone_records_chart
from phonedb.models import Connection, Feature, Phone, Vendor


class PhoneDBTest(TestCase):
    def setUp(self):
        cache.clear()
        self.vendor = Vendor.objects.create(
            name="Test",
            slug="test",
            url="https://example.com",
        )
        Feature.objects.create(name="info")
        self.connection = Connection.objects.create(name="at", medium="usb")
        Site.objects.create(name="testserver", domain="testserver")

    def test_index(self):
        response = self.client.get(reverse("phonedb"))
        self.assertContains(response, reverse("phonedb-chart"))
        self.assertNotContains(response, "google.com/chart")
        self.assertContains(response, 'class="site-form site-form--horizontal"')
        self.assertContains(response, 'name="q"')
        self.assertContains(response, 'name="feature"')
        self.assertContains(response, ">Search</button>")

    def test_chart(self):
        response = self.client.get(reverse("phonedb-chart"))

        self.assertEqual(response["Content-Type"], "image/svg+xml")
        self.assertNotContains(response, "google.com")
        root = ET.fromstring(response.content)
        namespace = {"svg": "http://www.w3.org/2000/svg"}
        self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")
        self.assertEqual(root.attrib["viewBox"], "0 0 800 300")
        polylines = root.findall(".//svg:polyline", namespace)
        self.assertEqual(
            {polyline.attrib["class"] for polyline in polylines},
            {
                "series supported-phones",
                "series approved-records",
                "series total-records",
            },
        )
        self.assertEqual(
            {
                polyline.attrib["class"]: polyline.attrib["stroke"]
                for polyline in polylines
            },
            {
                "series supported-phones": "#009e73",
                "series approved-records": "#b7791f",
                "series total-records": "#0072b2",
            },
        )
        self.assertTrue(
            all(polyline.attrib["stroke-linecap"] == "round" for polyline in polylines),
        )
        chart_text = "".join(root.itertext())
        self.assertIn("Supported phones", chart_text)
        self.assertIn("Approved records", chart_text)
        self.assertIn("Total records", chart_text)

    def test_chart_data(self):
        phone = Phone.objects.create(
            vendor=self.vendor,
            name="Chart phone",
            connection=self.connection,
            state="approved",
        )
        Phone.objects.filter(pk=phone.pk).update(
            created=datetime.datetime(
                2006,
                1,
                15,
                tzinfo=datetime.timezone.utc,
            ),
        )

        response = self.client.get(reverse("phonedb-chart"))
        root = ET.fromstring(response.content)
        polylines = root.findall(
            ".//svg:polyline",
            {"svg": "http://www.w3.org/2000/svg"},
        )
        for polyline in polylines:
            y_values = {
                float(point.split(",")[1])
                for point in polyline.attrib["points"].split()
            }
            self.assertGreater(len(y_values), 1)

    def test_chart_legacy_redirect(self):
        response = self.client.get(reverse("phonedb-chart-legacy"))

        self.assertRedirects(
            response,
            reverse("phonedb-chart"),
            status_code=301,
            fetch_redirect_response=False,
        )

    @mock.patch("phonedb.charts.render_phone_records_chart")
    def test_chart_cache(self, render_chart):
        render_chart.side_effect = [b"english", b"czech", b"refreshed"]

        with translation.override("en"):
            self.assertEqual(get_phone_records_chart(), b"english")
            self.assertEqual(get_phone_records_chart(), b"english")
        with translation.override("cs"):
            self.assertEqual(get_phone_records_chart(), b"czech")
        with translation.override("en"):
            self.assertEqual(get_phone_records_chart(force=True), b"refreshed")

        self.assertEqual(render_chart.call_count, 3)

    @mock.patch(
        "phonedb.management.commands.update_charts_url.get_phone_records_chart",
    )
    def test_update_chart_command(self, get_chart):
        call_command("update_charts_url")

        get_chart.assert_called_once_with(force=True)

    def test_add(self):
        response = self.client.post(
            reverse("phonedb-new"),
            {
                "vendor": "1",
                "name": "TestPHone",
                "connection": "1",
                "model": "",
                "features": "1",
                "gammu_version": "1.2.3",
                "note": "",
                "author_name": "Nobody",
                "author_email": "noreply@example.com",
                "email_garble": "atdot",
                "irobot": "nospam",
            },
            follow=True,
        )
        self.assertContains(response, "Phone record has been created.")
        self.assertContains(response, "Test TestPHone")

    def test_add_wammu(self):
        response = self.client.post(
            reverse("phonedb-api"),
            {
                "manufacturer": "1",
                "name": "TestPHone",
                "connection": "at",
                "model": "",
                "features": "1",
                "gammu_version": "1.2.3",
                "note": "",
                "author_name": "Nobody",
                "author_email": "noreply@example.com",
                "email_garble": "atdot",
                "irobot": "wammu",
            },
        )
        self.assertContains(response, "Entry created")

    def test_add_wammu_missing(self):
        response = self.client.post(
            reverse("phonedb-api"),
        )
        self.assertContains(response, "Invalid values")
        self.assertContains(response, "gammu_version")

    def test_add_prefill(self):
        response = self.client.get(
            reverse("phonedb-new"),
            {
                "vendor": "test",
                "name": "TestingPHone",
            },
        )
        self.assertContains(response, "TestingPHone")
        self.assertContains(response, '<option value="1" selected')

    def test_add_form_errors(self):
        response = self.client.post(
            reverse("phonedb-new"),
            {"irobot": "nospam"},
        )

        self.assertContains(response, "form-field--invalid")
        self.assertContains(response, 'aria-invalid="true"')
        self.assertContains(response, 'id="id_name_helptext"')
        self.assertContains(response, ">Save</button>")

    def test_csv(self):
        self.test_add()
        response = self.client.get(reverse("phonedb-csv"))
        self.assertEqual(response.get("Content-Type"), "text/csv")
        self.assertContains(response, "TestPHone")
        self.assertContains(response, "noreply[at]example[dot]com")

    def test_search(self):
        response = self.client.get(reverse("phonedb-search"), {"feature": "1"})
        self.assertContains(response, "Found 0 results matching your query.")
        response = self.client.get(
            reverse("phonedb-search-feature", kwargs={"featurename": "info"}),
        )
        self.assertContains(response, "Found 0 results matching your query.")

        self.test_add()

        response = self.client.get(reverse("phonedb-search"), {"feature": "1"})
        self.assertContains(response, "TestPHone")
        response = self.client.get(
            reverse("phonedb-search-feature", kwargs={"featurename": "info"}),
        )
        self.assertContains(response, "TestPHone")

    def test_vendor_list(self):
        self.test_add()
        response = self.client.get(
            reverse("phonedb-vendor", kwargs={"vendorname": "test"}),
        )
        self.assertContains(response, "TestPHone")

    def test_feed(self):
        self.test_add()
        response = self.client.get(
            reverse("phonedb-rss"),
            headers={"host": "testserver"},
        )
        self.assertContains(response, "TestPHone")
