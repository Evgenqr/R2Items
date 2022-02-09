from django.forms import ModelForm
from .models import Item, Monster, Location, Category, Comments


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


class CommentForm(ModelForm):
    """Форма комментариев"""
    class Meta:
        model = Comments
        fields = ("text", )
