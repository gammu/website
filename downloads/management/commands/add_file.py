from django.core.management.base import BaseCommand, CommandError
import hashlib
import os
from downloads.models import Release, Download


class Command(BaseCommand):
    help = 'adds file to the release'
    args = '<base> <program> <version> <type> <file>...'

    def handle(self, *args, **options):
        if len(args) < 5:
            raise CommandError('Usage: add_file /base/path program version type file...')

        release = Release.objects.get(program = args[1], version = args[2])

        dlpath = args[0]

        while dlpath[-1] == '/':
            dlpath = dlpath[:-1]

        for f in args[4:]:
            print "Adding %s..." % f
            path, filename = os.path.split(f)

            data = open(f).read()

            dl = Download()
            dl.release = release

            md5 = hashlib.md5()
            md5.update(data)
            dl.md5 = md5.hexdigest()

            sha1 = hashlib.sha1()
            sha1.update(data)
            dl.sha1 = sha1.hexdigest()

            dl.size = len(data)

            dl.platform = args[3]

            dl.location = '%s/%s' % (dlpath, filename)

            dl.save()
