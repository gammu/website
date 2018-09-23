# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pub_date', models.DateTimeField(default=datetime.datetime.today, verbose_name='Date posted')),
                ('slug', models.SlugField(help_text='Used in the URL of the entry. Must be unique for the publication date of the entry.', unique_for_date=b'pub_date')),
                ('title', models.CharField(max_length=250)),
                ('body', models.TextField()),
                ('body_html', models.TextField(editable=False, blank=True)),
                ('excerpt', models.TextField(null=True, blank=True)),
                ('excerpt_html', models.TextField(null=True, editable=False, blank=True)),
                ('identica_post', models.NullBooleanField(default=False, verbose_name=b'post to identi.ca')),
                ('identica_text', models.CharField(max_length=100, null=True, verbose_name=b'identi.ca post text', blank=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.deletion.CASCADE)),
                ('categories', models.ManyToManyField(to='news.Category')),
            ],
            options={
                'ordering': ['-pub_date'],
                'get_latest_by': 'pub_date',
                'verbose_name_plural': 'Entries',
            },
            bases=(models.Model,),
        ),
    ]
