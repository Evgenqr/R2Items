from django.shortcuts import render
from django import views
from .models import Item, Location, Monster


def ItemList(request):
    items = Item.objects.all()
    return render(request, 'items/index.html', {'items': items})


class LocationsView(views.View):
    def get(self, request, *args, **kwargs):
        locations = Location.objects.all()
        context = {
            'locations': locations
            }
        return render(request, 'items/index.html', context)


class ItemsView(views.View):
    def get(self, request, *args, **kwargs):
        items = Item.objects.all()
        context = {
            'items': items
         }
        return render(request, 'items/items.html', context)


class MonstersView(views.View):
    def get(self, request, *args, **kwargs):
        monsters = Monster.objects.all()
        context = {
            'monsters': monsters
         }
        return render(request, 'items/monsters.html', context)


class ItemDetailView(views.generic.DetailView):
    model = Item
    template_name = 'items/subpage.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'item'
