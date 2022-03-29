from django.contrib import admin
from .models import Location, Monster, Category, Item

   
class LocationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user']
    # prepopulated_fields = {'slug': ('title', )}
    list_filter = ['title']
    prepopulated_fields = {'slug': ('title',)}


class MonsterAdmin(admin.ModelAdmin):
    list_display = ['name', 'user']
    prepopulated_fields = {'slug': ('name', )}
    list_filter = ['name']


class ItemAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'category',
        'slug',
        'user'
    ]
    prepopulated_fields = {'slug': ('name', )}
    list_filter = ['name', 'category', 'monster']
    list_editable = ['category', 'slug']


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
