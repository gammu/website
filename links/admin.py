from django.contrib import admin

from links.models import Link


class LinkAdmin(admin.ModelAdmin):
    list_display = ("title", "url")
    search_fields = ("description", "url", "title")


admin.site.register(Link, LinkAdmin)
