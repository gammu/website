from phonedb.models import Vendor, Feature, Connection, Phone
from django.contrib import admin

class VendorAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('name', )
    }
    list_display = ('name', 'url', 'slug', 'tuxmobil')

admin.site.register(Vendor, VendorAdmin)

admin.site.register(Feature)

class ConnectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'medium')
    list_filter = ('medium', )

admin.site.register(Connection, ConnectionAdmin)

class PhoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor', 'connection', 'author_email', 'state')
    list_filter = ('state', 'vendor')

admin.site.register(Phone, PhoneAdmin)

