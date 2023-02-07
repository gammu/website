from django.db import migrations, models

import phonedb.models


class Migration(migrations.Migration):
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Connection",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("name", models.CharField(max_length=250)),
                (
                    "medium",
                    models.CharField(
                        max_length=100,
                        choices=[
                            ("usb", "USB"),
                            ("serial", "Serial"),
                            ("irda", "IrDA"),
                            ("bluetooth", "Bluetooth"),
                            ("other", "Other"),
                        ],
                    ),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Feature",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("name", models.CharField(max_length=250)),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Phone",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Phone name, please exclude vendor name.",
                        max_length=250,
                        validators=[phonedb.models.phone_name_validator],
                    ),
                ),
                (
                    "model",
                    models.CharField(
                        help_text="Model used in Gammu configuration, usually empty.",
                        max_length=100,
                        blank=True,
                    ),
                ),
                (
                    "gammu_version",
                    models.CharField(
                        help_text="Gammu version where you tested this phone.",
                        max_length=100,
                        blank=True,
                    ),
                ),
                (
                    "note",
                    models.TextField(
                        help_text='Any note about this phone and Gammu support for it. You can use <a href="http://daringfireball.net/projects/markdown/syntax">markdown markup</a>.',
                        blank=True,
                    ),
                ),
                ("note_html", models.TextField(editable=False, blank=True)),
                ("author_name", models.CharField(max_length=250, blank=True)),
                (
                    "author_email",
                    models.EmailField(
                        help_text="Please choose how will be email handled in next field.",
                        max_length=250,
                        blank=True,
                    ),
                ),
                (
                    "email_garble",
                    models.CharField(
                        default="atdot",
                        max_length=100,
                        choices=[
                            ("atdot", "Use [at] and [dot]"),
                            ("none", "Display it normally"),
                            ("hide", "Don't show email at all"),
                            ("nospam", "Insert NOSPAM text at random position"),
                        ],
                    ),
                ),
                (
                    "state",
                    models.CharField(
                        default="draft",
                        max_length=100,
                        db_index=True,
                        choices=[
                            ("draft", "Draft"),
                            ("approved", "Approved"),
                            ("deleted", "Deleted"),
                        ],
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("address", models.CharField(max_length=100, blank=True)),
                ("hostname", models.CharField(max_length=100, blank=True)),
                (
                    "connection",
                    models.ForeignKey(
                        blank=True,
                        to="phonedb.Connection",
                        help_text="Connection used in Gammu configuration.",
                        null=True,
                        on_delete=models.deletion.CASCADE,
                    ),
                ),
                (
                    "features",
                    models.ManyToManyField(
                        help_text="Features which are working in Gammu.",
                        to="phonedb.Feature",
                        blank=True,
                    ),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Vendor",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("name", models.CharField(max_length=250)),
                ("url", models.URLField(max_length=250)),
                ("slug", models.SlugField(unique=True)),
                ("tuxmobil", models.SlugField(null=True, blank=True)),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name="phone",
            name="vendor",
            field=models.ForeignKey(
                to="phonedb.Vendor", on_delete=models.deletion.CASCADE
            ),
            preserve_default=True,
        ),
    ]
