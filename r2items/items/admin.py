from django.contrib import admin
from .models import Location, Monster, Category, Item, Reviews

   
class LocationAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title', ), 'url': ('title', )}
    list_filter = ['title']
    list_editable = ['slug']


class MonsterAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name', ), 'url': ('name', )}
    list_filter = ['name']
    list_editable = ['slug']


class ItemAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'category',
        'url',
        'slug'
    ]
    prepopulated_fields = {'slug': ('name', ), 'url': ('name', )}
    list_filter = ['name', 'category', 'monster']
    list_editable = ['category', 'url', 'slug']


admin.site.register(Location, LocationAdmin)
admin.site.register(Monster, MonsterAdmin)
admin.site.register(Category)
admin.site.register(Item, ItemAdmin)
admin.site.register(Reviews)
