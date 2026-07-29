"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase

from wammu.helpers import render_markdown


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """Tests that 1 + 1 always equals 2."""
        self.assertEqual(1 + 1, 2)

    def test_github_urls_are_linked_in_markdown(self):
        url = "https://github.com/gammu/python-gammu/pull/123"
        rendered = render_markdown(
            f"Bare {url}. Existing [{url}]({url}) and <{url}>.",
        )

        self.assertEqual(rendered.count(f'href="{url}"'), 3)
        self.assertIn(f'<a href="{url}">{url}</a>.', rendered)


__test__ = {
    "doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
""",
}
