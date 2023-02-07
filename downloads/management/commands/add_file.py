import hashlib
import os

from django.core.management.base import BaseCommand

from downloads.models import Download, Release


class Command(BaseCommand):
    help = "adds file to the release"

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument("base")
        parser.add_argument("program")
        parser.add_argument("version")
        parser.add_argument("type")
        parser.add_argument("file", nargs="+")

    def handle(self, *args, **options):
        release = Release.objects.get(
            program=options["program"], version=options["version"]
        )

        dlpath = options["base"]

        while dlpath[-1] == "/":
            dlpath = dlpath[:-1]

        for f in options["file"]:
            self.stdout.write("Adding %s..." % f)
            filename = os.path.basename(f)

            with open(f, "rb") as handle:
                data = handle.read()

            dl = Download()
            dl.release = release

            md5 = hashlib.md5()
            md5.update(data)
            dl.md5 = md5.hexdigest()

            sha1 = hashlib.sha1()
            sha1.update(data)
            dl.sha1 = sha1.hexdigest()

            sha256 = hashlib.sha256()
            sha256.update(data)
            dl.sha256 = sha256.hexdigest()

            dl.size = len(data)

            dl.platform = options["type"]

            dl.location = f"{dlpath}/{filename}"

            dl.save()
