from django.test import TestCase
from django.urls import reverse


class ToolsTest(TestCase):
    def test_pdudecode(self):
        response = self.client.post(reverse("pdudecode"), {"text": "xxx"})
        self.assertContains(response, "Enter a valid value.")
        response = self.client.post(
            reverse("pdudecode"),
            {
                "text": "0791361907001003B17A0C913619397750320000AD11CD701E340FB3C3F23CC81D0689C3BF"
            },
        )
        self.assertContains(response, "Message number 1")
        self.assertContains(response, "+639170000130")

    def test_pduencode(self):
        response = self.client.post(
            reverse("pduencode"),
            {"text": "Test", "number": "800123456", "cls": "0", "smsc": "800123456"},
        )
        self.assertContains(
            response, "068108103254f61100098108103254f600f0ff04d4f29c0e"
        )

    def test_countries(self):
        response = self.client.get(reverse("countries"))
        self.assertContains(response, "Zimbabwe")

    def test_networks(self):
        response = self.client.get(reverse("networks"))
        self.assertContains(response, "GammuTel")
