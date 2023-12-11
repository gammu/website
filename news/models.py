import datetime

import markdown
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    """A category that an entry can belong to."""

    title = models.CharField(max_length=250)
    slug = models.SlugField(
        unique=True, help_text="Used in the URL for the category. Must be unique."
    )
    description = models.TextField(
        help_text="A short description of the category, to be used in list pages."
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
        return reverse("news-category", kwargs={"slug": self.slug})


class Entry(models.Model):
    # Metadata.
    author = models.ForeignKey(User, on_delete=models.deletion.CASCADE)
    pub_date = models.DateTimeField(
        "Date posted",
        default=datetime.datetime.today,
        db_index=True,
    )
    slug = models.SlugField(
        unique_for_date="pub_date",
        help_text="Used in the URL of the entry. Must be unique for the publication date of the entry.",
    )
    title = models.CharField(max_length=250)

    # The actual entry bits.
    body = models.TextField()
    body_html = models.TextField(editable=False, blank=True)
    excerpt = models.TextField(blank=True, null=True)
    excerpt_html = models.TextField(blank=True, null=True, editable=False)

    # Categorization.
    categories = models.ManyToManyField(Category, blank=False)

    class Meta:
        get_latest_by = "pub_date"
        ordering = ["-pub_date"]
        verbose_name_plural = "Entries"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.pub_date is None:
            self.pub_date = timezone.now()
        if self.excerpt:
            self.excerpt_html = markdown.markdown(self.excerpt)
        self.body_html = markdown.markdown(self.body, safe_mode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "news-entry",
            kwargs={
                "year": self.pub_date.strftime("%Y"),
                "month": self.pub_date.strftime("%m"),
                "day": self.pub_date.strftime("%d"),
                "slug": self.slug,
            },
        )
