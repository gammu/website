from wammu_web.downloads.models import Mirror, Program, Release, DownloadType, Download, DownloadKind, ReleaseType
from django.contrib import admin

class MirrorAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('name', )
    }

admin.site.register(Mirror, MirrorAdmin)

class ProgramAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('name', )
    }

admin.site.register(Program, ProgramAdmin)
admin.site.register(DownloadKind)
admin.site.register(DownloadType)
admin.site.register(Download)
admin.site.register(Release)
admin.site.register(ReleaseType)
