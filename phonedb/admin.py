from django.contrib import admin

from phonedb.models import Connection, Feature, Phone, Vendor


class VendorAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "url", "slug")
    search_fields = ["name", "url", "slug"]


admin.site.register(Vendor, VendorAdmin)

admin.site.register(Feature)


class ConnectionAdmin(admin.ModelAdmin):
    list_display = ("name", "medium")
    list_filter = ("medium",)
    search_fields = ["name", "medium"]


admin.site.register(Connection, ConnectionAdmin)


class PhoneAdmin(admin.ModelAdmin):
    list_display = ("name", "vendor", "connection", "author_email", "state", "created")
    list_filter = ("state", "vendor")
    search_fields = ["name", "author_email", "note", "model"]


admin.site.register(Phone, PhoneAdmin)
