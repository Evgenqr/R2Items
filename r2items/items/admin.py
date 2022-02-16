from django.contrib import admin
from .models import Location, Monster, Category, Item#, Reviews

   
class LocationAdmin(admin.ModelAdmin):
    list_display = ['title']
    prepopulated_fields = {'url': ('title', )}
    list_filter = ['title']


class MonsterAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    prepopulated_fields = {'url': ('name', )}
    list_filter = ['name']


class ItemAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'category',
        'url',
    ]
    prepopulated_fields = {'url': ('name', )}
    list_filter = ['name', 'category', 'monster']
    list_editable = ['category', 'url']


# class ReviewsAdmin(admin.ModelAdmin):
#     list_display = [
#         'name',
#         'monster',
#         'text'
#     ]


admin.site.register(Location, LocationAdmin)
admin.site.register(Monster, MonsterAdmin)
admin.site.register(Category)
admin.site.register(Item, ItemAdmin)
# admin.site.register(Reviews, ReviewsAdmin)
