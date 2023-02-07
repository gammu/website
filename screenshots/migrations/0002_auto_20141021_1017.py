from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("screenshots", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="screenshot",
            name="featured",
            field=models.BooleanField(default=False),
        ),
    ]
