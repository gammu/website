import markdown
from django.db import models
from django.urls import reverse

from screenshots.thumbs import ImageWithThumbsField


class Category(models.Model):
    """A category that an entry can belong to."""

    title = models.CharField(max_length=250)
    slug = models.SlugField(
        unique=True,
        help_text="Used in the URL for the category. Must be unique.",
    )
    description = models.TextField(
        help_text="A short description of the category, to be used in list pages.",
    )
    description_html = models.TextField(editable=False, blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["title"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.description_html = markdown.markdown(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("screenshots-category", kwargs={"slug": self.slug})


class Screenshot(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    description_html = models.TextField(editable=False, blank=True)
    image = ImageWithThumbsField(upload_to="screenshots", sizes=((180, 120),))
    featured = models.BooleanField(default=False)

    # Categorization.
    categories = models.ManyToManyField(Category, blank=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.description_html = markdown.markdown(self.description)
        super().save(*args, **kwargs)
