from django.contrib import admin

from phonedb.models import Connection, Feature, Phone, Vendor


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "url", "slug")
    search_fields = ["name", "url", "slug"]


admin.site.register(Feature)


@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    list_display = ("name", "medium")
    list_filter = ("medium",)
    search_fields = ["name", "medium"]


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ("name", "vendor", "connection", "author_email", "state", "created")
    list_filter = ("state", "vendor")
    search_fields = ["name", "author_email", "note", "model"]
