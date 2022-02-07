from django.shortcuts import render
from django import views
from .models import Item, Location, Monster


class LocationsView(views.View):
    def get(self, request, *args, **kwargs):
        locations = Location.objects.all()
        monsters = Monster.objects.all()
        context = {
            'locations': locations,
            'monsters': monsters
            }
        return render(request, 'items/index.html', context)


def get_local(request, slug):
    slug = Location.objects.get(slug=slug)
    if slug:
        monsters = Monster.objects.filter(locations=slug)
    else:
        monsters = Monster.objects.all()
    locations = Location.objects.all()
    context = {
        'monsters': monsters,
        'locations': locations
    }
    return render(request, 'items/locations.html', context)


def get_items(request, slug):
    slug = Monster.objects.get(slug=slug)
    if slug:
        items = Item.objects.filter(monster=slug)
    else:
        items = Item.objects.all()
    monsters = Monster.objects.all()
    context = {
        'items': items,
        'monsters': monsters
    }
    return render(request, 'items/monsters.html', context)
