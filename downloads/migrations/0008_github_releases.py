from django.db import migrations, models
from django.utils import timezone


class Migration(migrations.Migration):
    dependencies = [
        ("downloads", "0007_auto_20170614_1003"),
    ]

    operations = [
        migrations.AlterField(
            model_name="download",
            name="location",
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name="download",
            name="md5",
            field=models.CharField(blank=True, default="", max_length=250),
        ),
        migrations.AlterField(
            model_name="download",
            name="sha1",
            field=models.CharField(blank=True, default="", max_length=250),
        ),
        migrations.AlterField(
            model_name="download",
            name="sha256",
            field=models.CharField(blank=True, default="", max_length=250),
        ),
        migrations.AlterField(
            model_name="release",
            name="date",
            field=models.DateTimeField(default=timezone.now),
        ),
        migrations.AddConstraint(
            model_name="release",
            constraint=models.UniqueConstraint(
                fields=("program", "version"),
                name="unique_program_version",
            ),
        ),
    ]
