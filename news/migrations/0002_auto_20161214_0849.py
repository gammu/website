# Generated by Django 1.10.3 on 2016-12-14 08:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="entry",
            name="identica_post",
        ),
        migrations.RemoveField(
            model_name="entry",
            name="identica_text",
        ),
    ]
