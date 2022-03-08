from django.shortcuts import redirect, render, get_object_or_404
from django import views
from .models import Item, Location, Monster
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import LocationForm, ItemForm, MonsterForm
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.http import HttpResponse
from django.utils.text import slugify
from transliterate import translit


# ---- Location

class LocationsView(ListView):

    model = Location
    template_name = 'items/index.html'
    context_object_name = 'locations'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context
    
# class LocationsView(views.View):

#     def get(self, request, *args, **kwargs):
#         locations = Location.objects.all()
#         # locations = Location.objects.filter(user=request.user)
#         monsters = Monster.objects.all()
#         context = {'locations': locations, 'monsters': monsters}
#         return render(request, 'items/index.html', context)


@login_required
def createlocation(request):
    if request.method == 'GET':
        return render(request, 'items/createlocation.html',
                      {'form': LocationForm()})
    else:
        try:
            form = LocationForm(request.POST, request.FILES)
            newlocaltion = form.save(commit=False)
            # newlocaltion.url = request.user
            newlocaltion.user = request.user
            newlocaltion.url = translit(newlocaltion.title, language_code='ru', reversed=True)
            print('!!!',newlocaltion.url)
            newlocaltion.url = slugify(newlocaltion.url)
            print('----',newlocaltion.url)
            newlocaltion.save()
            return redirect('home')
        except ValueError:
            return render(request, 'items/createlocation.html', {
                'form': LocationForm(),
                'error': 'Bad data passed in'
            })


@login_required
def viewlocation(request, slug):
    location = get_object_or_404(Location, url=slug)

    print('vvvvvvvvv', location.user)
    print('request.user', request.user)

    if location.user == request.user:
        # location = Location.objects.filter(url=slug, user=request.user)
        if request.method == 'GET':
            form = LocationForm(instance=location)
            return render(request, 'items/viewlocation.html', {
                'location': location,
                'form': form
            })
        else:
            try:
                form = LocationForm(request.POST,
                                    request.FILES,
                                    instance=location)
                form.save()
                return redirect('home')
            except ValueError:
                return render(
                    request, 'items/viewlocation.html', {
                        'location': location,
                        'form': LocationForm(),
                        'error': 'Bad info'
                    })
    else:
        return HttpResponse("Here's the text of the Web page.")


@login_required
def deletelocation(request, slug):
    location = get_object_or_404(Location, url=slug)
    if request.method == 'POST':
        location.delete()
        return redirect('home')


# ---- Location END

# ---- Monster

class MonstersInLocation(ListView):

    model = Monster
    template_name = 'items/location_detail.html'
    context_object_name = 'monsters'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Location.objects.get(url=self.kwargs['slug'])
        return context

    def get_queryset(self):
        slug = Location.objects.get(url=self.kwargs['slug'])
        if slug:
            return Monster.objects.filter(locations=slug)


# def location_detail(request, slug):
#     slug = Location.objects.get(url=slug)
#     locations = Location.objects.all()
#     if slug:
#         monsters = Monster.objects.filter(locations=slug)
#     else:
#         monsters = Monster.objects.all()
#     context = {'monsters': monsters, 'locations': locations}
#     return render(request, 'items/location_detail.html', context)


@login_required
class AddMonster(FormView):
    template_name = "items/createmonster.html"
    form_class = MonsterForm
    success_url = '/'

    def form_valid(self, slug):
        slug = Location.objects.get(url=slug)
        print('slug ', slug)
        # locations = Location.objects.all()
        monsters = Monster.objects.filter(locations=slug)
        instance = Monster.objects.create(locations=slug)
        instance.locations.add(*monsters)
        return redirect("/")


class Set_user(FormView):
    template_name = "items/createmonster.html"
    form_class = MonsterForm
    success_url = '/'

    def form_valid(self, form):
        name = form.cleaned_data.get('name')
        instance = Monster(name=name, locations=location)
        instance.save()
        instance.location.add(request.location.title)
        instance.save()
        return redirect("/")


@login_required
def createmonster(request, slug):
    slug = Location.objects.get(url=slug)
    if request.method == 'POST':
        form = MonsterForm(request.POST, request.FILES)
        if form.is_valid():
            new_monster = form.save(commit=False)
            new_monster.save()
            new_monster.locations.add(slug)
    else:
        form = MonsterForm()
    return render(request, 'items/createmonster.html', {'form': form})


# @login_required
# def createmonster(request):
#     location = Location.objects.get(url=location)
#     print('location ', location)
#     # monster = location.
#     if request.method == 'GET':
#         return render(request, 'items/createmonster.html',
#                       {'location': location, 'form': MonsterForm()})
#     else:
#         try:
#             form = MonsterForm(request.POST, request.FILES)
#             if form.is_valid:
#                 newmonster = form.save(commit=False)
#                 newmonster.user = request.user
#                 newmonster.save()
#                 return redirect('home')
#         except ValueError:
#             return render(request, 'items/createmonster.html', {
#                 'location': location,
#                 'monster': monster,
#                 'form': MonsterForm(),
#                 'error': 'Bad data passed in'
#             })


@login_required
def viewmonster(request, slug):
    monster = get_object_or_404(Monster, url=slug)
    if request.method == 'GET':
        form = MonsterForm(instance=monster)
        return render(request, 'items/viewmonster.html', {
            'monster': monster,
            'form': form
        })
    else:
        try:
            form = MonsterForm(request.POST, request.FILES, instance=monster)
            form.save()
            return redirect('home')
        except ValueError:
            return render(request, 'items/viewmonster.html', {
                'monster': monster,
                'form': MonsterForm(),
                'error': 'Bad info'
            })


@login_required
def deletemonster(request, slug):
    monster = get_object_or_404(Monster, url=slug)
    if request.method == 'POST':
        monster.delete()
        return redirect('home')


# ---- Monster END

    # def get_queryset(self):
    #     slug = Location.objects.get(url=self.kwargs['slug'])
    #     if slug:
    #         return Monster.objects.filter(locations=slug)

# ---- Item

class ItemInMonster(ListView):

    model = Item
    template_name = 'items/monster_detail.html'
    context_object_name = 'items'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Monster.objects.get(url=self.kwargs['slug'])
        return context

    def get_queryset(self):
        slug = Monster.objects.get(url=self.kwargs['slug'])
        if slug:
            return Item.objects.filter(monster=slug)


class ItemDetail(DetailView):
    model = Item
    # slug_url_kwarg = 'url'
    template_name = 'items/item_detail.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Item.objects.get(slug=self.kwargs['slug'])
        return context

    # def get_queryset(self):
    #     slug = Monster.objects.get(url=self.kwargs['slug'])
    #     if slug:
    #         return Item.objects.filter(monster=slug)

# def monster_detail(request, slug):
#     slug = Monster.objects.get(url=slug)
#     locations = Location.objects.all()
#     print('!!!!!', slug)
#     if slug:
#         items = Item.objects.filter(monster=slug)
#     else:
#         items = Item.objects.all()
#     monsters = Monster.objects.all()
#     context = {'items': items, 'monsters': monsters, 'locations': locations}
#     return render(request, 'items/monster_detail.html', context)


@login_required
def createitem(request, slug):
    slug = Monster.objects.get(url=slug)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.save()
            new_item.monster.add(slug)
    else:
        form = ItemForm()
    return render(request, 'items/createitem.html', {'form': form})


# ---- Item END


# ---- User
def signupuser(request):
    if request.method == 'GET':
        return render(request, 'items/signupuser.html',
                      {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'],
                    password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('/')
            except IntegrityError:
                return render(
                    request, 'items/signupuser.html', {
                        'form': UserCreationForm(),
                        'error': 'That username has already been taken'
                    })
        else:
            return render(request, 'items/signupuser.html', {
                'form': UserCreationForm(),
                'error': 'Password did not match'
            })


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'items/loginuser.html',
                      {'form': AuthenticationForm()})
    else:
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password'],
        )
        if user is None:
            return render(
                request, 'items/loginuser.html', {
                    'form': AuthenticationForm(),
                    'error': 'User or password did not match'
                })
        else:
            login(request, user)
            return redirect('/')


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/')


# ---- User END

# def get_comment(request):
#     slug = Monster.objects.all()
#     if slug:
#         items = Item.objects.filter(monster=slug)
#         if request.method == 'POST':
#             form = CommentForm(request.POST)
#             if form.is_valid():
#                 form.save()
#                 return HttpResponseRedirect(request.path_info)

#         else:
#             form = CommentForm()
#             names = Reviews.objects.all()
#     else:
#         items = Item.objects.all()
#     monsters = Monster.objects.all()
#     comments = Reviews.objects.all()
#     return render(request, 'items/name.html', {
#         'form': form,
#         'names': names,
#         'monsters': monsters,
#         'items': items,
#         'comments': comments
#     })

# def get_items(request, slug):
#     slug = Monster.objects.get(slug=slug)
#     if slug:
#         items = Item.objects.filter(monster=slug)
#     else:
#         items = Item.objects.all()
#     monsters = Monster.objects.all()
#     context = {'items': items, 'monsters': monsters}
#     return render(request, 'items/monsters.html', context)
