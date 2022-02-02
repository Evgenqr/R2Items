from re import template
from django.shortcuts import render
from django import views
from .models import Item

def ItemList(request):
    items = Item.objects.all()
    return render(request, 'items/index.html', {'items': items})


class BaseView(views.View):
    def get(self, request, *args **kwargs):
        return render(request, 'index.html', {})
    
    
class ItemDetailView(views.generic.DetailView):
    model = Item
    template_name = 'items/subpage.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'item'
