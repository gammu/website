import markdown
from django.db import models

from screenshots.models import Screenshot


class Link(models.Model):
    title = models.CharField(max_length=250)
    url = models.URLField()
    screenshot = models.ForeignKey(
        Screenshot,
        null=True,
        blank=True,
        on_delete=models.deletion.CASCADE,
    )
    description = models.TextField()
    description_html = models.TextField(editable=False, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.description_html = markdown.markdown(self.description)
        super().save(*args, **kwargs)
