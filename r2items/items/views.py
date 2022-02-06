from msilib.schema import ListView
from django.shortcuts import render
from django import views
from .models import Item, Location, Monster
from django.views.generic import ListView


class MonsterItem:
    def get_monsters(self):
        return Monster.objects.all()

    def get_items(self):
        return Item.objects.values("monster")


class LocationsView(views.View):
    def get(self, request, *args, **kwargs):
        locations = Location.objects.all()
        monsters = Monster.objects.all()
        context = {
            'locations': locations,
            'monsters': monsters
            }
        return render(request, 'items/index.html', context)


def get_local(request, id):
    monsters = Monster.objects.filter(id=id)
    locations = Location.objects.all()
    locate = Location.objects.get(id=id)
    context = {
            'locations': locations,
            'monsters': monsters,
            'locate': locate
            }
    return render(request, 'items/monsters.html', context)


# class MonstersView(MonsterItem, views.View):

#     def get(self, location_id, request, *args, **kwargs):
#         monsters = Monster.objects.filter(location_id=location_id)
#         locations = Location.objects.all()
#         # locate = Location.objects.get(pk=location_id)
#         context = {
#             'locations': locations,
#             'monsters': monsters,
#             # 'locate': locate
#             }
#         return render(request, 'items/monsters.html', context)


class ItemsView(MonsterItem, views.View):
    def get(self, request, *args, **kwargs):
        items = Item.objects.all()
        context = {
            'items': items
         }
        return render(request, 'items/items.html', context)


class ItemDetailView(views.generic.DetailView):
    model = Item
    template_name = 'items/subpage.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'item'


class FilterMonstersView(MonsterItem, ListView):
    def get_queryset(self):
        queryset = Monster.objects.filter(location__in=self.request.GET.getlist("location"))
        return queryset
