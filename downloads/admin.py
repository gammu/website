from django.contrib import admin

from downloads.models import Download, Release

admin.site.register(Download)

admin.site.register(Release)
