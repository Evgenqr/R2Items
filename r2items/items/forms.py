from django.forms import ModelForm
from .models import Item, Monster, Location, Category#, Reviews


class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = ('title', 'local_img', 'slug', 'url')


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = [
            'name', 'description', 'weight', 'category', 'monster', 'item_img',
            'slug', 'url'
        ]


class MonsterForm(ModelForm):
    class Meta:
        model = Monster
        fields = ('name', 'description', 'monster_img', 'locations', 'slug',
                  'url')


class CategoryForm(ModelForm):
    model = Category
    fields = ['name']


# class ReviewForm(ModelForm):
#     """Форма отзывов"""
#     class Meta:
#         model = Reviews
#         fields = ("name", "email", "text")
