from django.contrib import admin

from screenshots.models import Category, Screenshot


class ScreenshotAdmin(admin.ModelAdmin):
    list_display = ("title", "image", "featured")
    list_filter = ("categories",)
    search_fields = ("image", "description", "title")


admin.site.register(Screenshot, ScreenshotAdmin)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Category, CategoryAdmin)
