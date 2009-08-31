from wammu_web.downloads.models import Mirror, Download, Release
from django.contrib import admin

class MirrorAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('name', )
    }

admin.site.register(Mirror, MirrorAdmin)

admin.site.register(Download)

admin.site.register(Release)
