from django.test import TestCase
from django.urls import reverse

from tools.forms import PDUDecodeForm


class ToolsTest(TestCase):
    def test_pdudecode_limits(self):
        self.assertTrue(PDUDecodeForm({"text": "00\n" * 49 + "00"}).is_valid())
        self.assertFalse(PDUDecodeForm({"text": "00\n" * 50 + "00"}).is_valid())
        self.assertTrue(PDUDecodeForm({"text": "00" * 256}).is_valid())
        self.assertFalse(PDUDecodeForm({"text": "00" * 257}).is_valid())

    def test_pdudecode_malformed_special_messages(self):
        for pdu in (
            "004000810004000000000000000807120500ffff0000",
            "00400081000400000000000000100b0504158a00000003ce010130017f7f",
        ):
            response = self.client.post(reverse("pdudecode"), {"text": pdu})
            self.assertEqual(response.status_code, 200)

    def test_pdudecode(self):
        response = self.client.post(reverse("pdudecode"), {"text": "xxx"})
        self.assertContains(response, "Enter a valid value.")
        self.assertContains(response, "form-field--invalid")
        self.assertContains(
            response, 'aria-describedby="id_text_helptext id_text_error"'
        )
        response = self.client.post(
            reverse("pdudecode"),
            {
                "text": "0791361907001003B17A0C913619397750320000AD11CD701E340FB3C3F23CC81D0689C3BF",
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
            response,
            "068108103254f61100098108103254f600f0ff04d4f29c0e",
        )

    def test_countries(self):
        response = self.client.get(reverse("countries"))
        self.assertContains(response, "Zimbabwe")

    def test_networks(self):
        response = self.client.get(reverse("networks"))
        self.assertContains(response, "GammuTel")
