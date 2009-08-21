from wammu_web.downloads.models import Mirror, Download
from django.contrib import admin

class MirrorAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('name', )
    }

admin.site.register(Mirror, MirrorAdmin)

admin.site.register(Download)
