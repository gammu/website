from django.contrib import admin

from links.models import Link


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ("title", "url")
    search_fields = ("description", "url", "title")
