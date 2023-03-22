from django.contrib import admin

from screenshots.models import Category, Screenshot


@admin.register(Screenshot)
class ScreenshotAdmin(admin.ModelAdmin):
    list_display = ("title", "image", "featured")
    list_filter = ("categories",)
    search_fields = ("image", "description", "title")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
