# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import screenshots.thumbs


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=250)),
                ('slug', models.SlugField(help_text='Used in the URL for the category. Must be unique.', unique=True)),
                ('description', models.TextField(help_text='A short description of the category, to be used in list pages.')),
                ('description_html', models.TextField(editable=False, blank=True)),
            ],
            options={
                'ordering': ['title'],
                'verbose_name_plural': 'Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Screenshot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('description_html', models.TextField(editable=False, blank=True)),
                ('image', screenshots.thumbs.ImageWithThumbsField(upload_to='screenshots')),
                ('featured', models.BooleanField()),
                ('categories', models.ManyToManyField(to='screenshots.Category')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
