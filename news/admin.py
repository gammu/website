from wammu_web.news.models import Category, Entry
from django.contrib import admin

class EntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    list_display = ('title', 'pub_date', 'author')
    list_filter = ('categories', )
    search_fields = ('excerpt', 'body', 'title')
    prepopulated_fields = {
        'slug': ('title', ),
        'identica_text': ('title', ),
    }

admin.site.register(Entry, EntryAdmin)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('title', )
    }

admin.site.register(Category, CategoryAdmin)
