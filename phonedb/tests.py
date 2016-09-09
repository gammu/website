from django.test import TestCase
from django.core.urlresolvers import reverse

from phonedb.models import Vendor, Feature, Connection


class PhoneDBTest(TestCase):
    def setUp(self):
        Vendor.objects.create(name='Test', slug='test', url='https://example.com')
        Feature.objects.create(name='info')
        Connection.objects.create(name='at', medium='usb')

    def test_index(self):
        response = self.client.get(reverse('phonedb'))
        self.assertContains(response, 'https://www.google.com/chart')

    def test_add(self):
        response = self.client.post(
            reverse('phonedb-new'),
            {
                'vendor': '1',
                'name': 'TestPHone',
                'connection': '1',
                'model': '',
                'features': '1',
                'gammu_version': '1.2.3',
                'note': '',
                'author_name': 'Nobody',
                'author_email': 'noreply@example.com',
                'email_garble': 'atdot',
                'irobot': 'nospam',
            },
            follow=True
        )
        self.assertContains(response, 'Phone record has been created.')

    def test_csv(self):
        self.test_add()
        response = self.client.get(reverse('phonedb-csv'))
        self.assertEqual(response.get('Content-Type'), 'text/csv')
        self.assertContains(response, 'TestPHone')
        self.assertContains(response, 'noreply[at]example[dot]com')
