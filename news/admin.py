from django.contrib import admin

from news.models import Category, Entry


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    date_hierarchy = "pub_date"
    list_display = ("title", "pub_date", "author")
    list_filter = ("categories",)
    search_fields = ("excerpt", "body", "title")
    prepopulated_fields = {
        "slug": ("title",),
    }


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
