import os
import os.path

import markdown
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy

from news.models import Category
from wammu.helpers import process_bug_links

PROGRAM_CHOICES = (
    ("gammu", "Gammu"),
    ("wammu", "Wammu"),
    ("python-gammu", "python-gammu"),
)

PROGRAM_URLS = {
    "gammu": "/gammu/",
    "wammu": "/wammu/",
    "python-gammu": "/python-gammu/",
}

PLATFORM_CHOICES = (
    ("source", gettext_lazy("Source code")),
    ("win32", gettext_lazy("Windows binaries")),
)


def get_latest_releases(program):
    """Returns tuple with last release information for given program.
    First is stable, second is testing, which can be None.
    """
    releases = Release.objects.filter(program=program)
    if releases.count() == 0:
        return (None, None)
    latest_version = releases.order_by("-version_int")[0]
    if latest_version.is_stable():
        latest_stable = latest_version
        latest_testing = None
    else:
        latest_testing = latest_version
        latest_stable = releases.filter(
            version_int__lt=10 + ((latest_version.version_int / 100) * 100)
        ).order_by("-version_int")[0]
    return (latest_stable, latest_testing)


def get_program(name):
    for c in PROGRAM_CHOICES:
        if c[0] == name:
            return c[1]
    raise IndexError("Program does not exist!")


def get_current_downloads(program):
    """Gets list of tuples for currently active downloads. The first one
    is always present and it's the stable one, the second one is
    testing if available.
    """
    downloads = []

    stable_release, testing_release = get_latest_releases(program)

    stable_downloads = Download.objects.filter(release=stable_release)

    downloads.append((stable_release, stable_downloads))

    if testing_release is not None:
        testing_downloads = Download.objects.filter(release=testing_release)
        downloads.append((testing_release, testing_downloads))

    return downloads


class Release(models.Model):
    author = models.ForeignKey(User, on_delete=models.deletion.CASCADE)
    program = models.CharField(max_length=100, choices=PROGRAM_CHOICES)
    version = models.CharField(max_length=100)
    version_int = models.IntegerField(editable=False, blank=True)
    description = models.TextField()
    description_html = models.TextField(editable=False, blank=True)
    changelog = models.TextField(blank=True, null=True)
    changelog_html = models.TextField(blank=True, null=True, editable=False)
    date = models.DateTimeField(auto_now_add=True)
    post_news = models.BooleanField(default=True)

    class Meta:
        ordering = ["-date"]

    def save(self, *args, **kwargs):
        version = self.version.split(".")
        self.version_int = 0
        for num in version:
            self.version_int = (100 * self.version_int) + int(num)
        # Implicit .0
        if len(version) == 2:
            self.version_int = 100 * self.version_int
        if self.post_news:
            author = self.author
            current_site = "wammu.eu"
            excerpt = "[{programname}]({programurl}) [{version}]({versionurl}) has been just released. {description}".format(
                programname=get_program(self.program),
                version=self.version,
                description=self.description,
                programurl="https://{}{}".format(
                    current_site, PROGRAM_URLS[self.program]
                ),
                versionurl=f"https://{current_site}{self.get_absolute_url()}",
            )
            body = (
                "Full list of changes:\n\n%s\n\nYou can download it from <https://wammu.eu/download/>.\n\nSupport this program by donations <https://wammu.eu/donate/>."
                % self.changelog
            )
            title = "{} {}".format(
                get_program(self.program),
                self.version,
            )
            slug = "{}-{}".format(
                self.program,
                self.version.replace(".", "-"),
            )
            category = Category.objects.get(slug=self.program)
            category.entry_set.create(
                author=author,
                excerpt=excerpt,
                body=process_bug_links(body),
                title=title,
                slug=slug,
            )
        self.post_news = False
        self.changelog_html = markdown.markdown(process_bug_links(self.changelog))
        self.description_html = markdown.markdown(self.description)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.program}-{self.version}"

    def is_stable(self):
        return self.version_int % 100 < 90

    def get_description(self):
        if self.is_stable():
            return _("%(program)s stable release %(version)s") % {
                "program": self.get_program(),
                "version": self.version,
            }
        return _("%(program)s testing release %(version)s") % {
            "program": self.get_program(),
            "version": self.version,
        }

    def get_program(self):
        return get_program(self.program)

    def get_absolute_url(self):
        return reverse(
            "downloads-release",
            kwargs={"version": self.version, "program": self.program},
        )


class Download(models.Model):
    release = models.ForeignKey(Release, on_delete=models.deletion.CASCADE)
    platform = models.CharField(max_length=100, choices=PLATFORM_CHOICES)
    location = models.CharField(max_length=250)
    md5 = models.CharField(max_length=250)
    sha1 = models.CharField(max_length=250)
    sha256 = models.CharField(max_length=250)
    size = models.IntegerField()

    class Meta:
        ordering = ["platform", "location"]

    def __str__(self):
        return f"{self.release} ({self.platform}): {self.location}"

    def get_filename(self):
        return os.path.split(self.location)[1]

    def get_size(self):
        if self.size > 4 * 1024 * 1024:
            return "%d MiB" % self.get_size_mib()
        if self.size > 4 * 1024:
            return "%d KiB" % self.get_size_kib()
        return "%d B" % self.size

    def get_size_mib(self):
        return self.size / (1024 * 1024)

    def get_size_kib(self):
        return self.size / (1024)
