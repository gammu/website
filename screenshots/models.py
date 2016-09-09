from django.db import models
import markdown
from thumbs import ImageWithThumbsField

# Create your models here.

class Category(models.Model):
    """
    A category that an entry can belong to.

    """
    title = models.CharField(
        max_length = 250
        )
    slug = models.SlugField(
        unique = True,
        help_text = u'Used in the URL for the category. Must be unique.'
        )
    description = models.TextField(
        help_text = u'A short description of the category, to be used in list pages.'
        )
    description_html = models.TextField(
        editable = False,
        blank = True
        )

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['title']

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.description_html = markdown.markdown(self.description)
        super(Category, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
         return ('screenshots-category', (), { 'slug': self.slug })


class Screenshot(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    description_html = models.TextField(
        editable = False,
        blank = True
        )
    image = ImageWithThumbsField(upload_to='screenshots', sizes=((180,120),))
    featured = models.BooleanField(default=False)

    # Categorization.
    categories = models.ManyToManyField(
        Category,
        blank = False
        )

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.description_html = markdown.markdown(self.description)
        super(Screenshot, self).save(*args, **kwargs)
