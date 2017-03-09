from django.db import models
from django.utils.encoding import python_2_unicode_compatible

import markdown

from screenshots.models import Screenshot


@python_2_unicode_compatible
class Link(models.Model):
    title = models.CharField(max_length=250)
    url = models.URLField()
    screenshot = models.ForeignKey(Screenshot, null = True, blank = True)
    description = models.TextField()
    description_html = models.TextField(
        editable = False,
        blank = True
        )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.description_html = markdown.markdown(self.description)
        super(Link, self).save(*args, **kwargs)
