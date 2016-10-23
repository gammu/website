from django.core.management.base import BaseCommand, CommandError
import hashlib
import os
from downloads.models import Release, Download


class Command(BaseCommand):
    help = 'adds file to the release'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('base')
        parser.add_argument('program')
        parser.add_argument('version')
        parser.add_argument('type')
        parser.add_argument('file', nargs='+')

    def handle(self, *args, **options):

        release = Release.objects.get(program=options['program'], version=options['version'])

        dlpath = options['base']

        while dlpath[-1] == '/':
            dlpath = dlpath[:-1]

        for f in options['file']:
            self.stdout.write("Adding %s..." % f)
            filename = os.path.basename(f)

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

            dl.platform = options['type']

            dl.location = '%s/%s' % (dlpath, filename)

            dl.save()
