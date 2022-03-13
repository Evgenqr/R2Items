from django.forms import ModelForm
from .models import Item, Monster, Location, Category  #, Reviews
from django import forms


class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = ('title', 'local_img')


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = [
            'name', 'description', 'weight', 'category', 'monster', 'item_img'
        ]


class MonsterForm(ModelForm):
    class Meta:
        model = Monster
        fields = ('name', 'description', 'monster_img', 'locations')
        # widgets = {
        #     'name': forms.TextInput(),
        #     'description': forms.Textarea(),
        #     'locations': forms.Select(),
        # }


class CategoryForm(ModelForm):
    model = Category
    fields = ['name']


# class CommentForm(ModelForm):
#     """Форма комментариев"""
#     class Meta:
#         model = Reviews
#         fields = ("text", )
