from django.shortcuts import redirect, render, get_object_or_404
from django import views
from .models import Item, Location, Monster, Reviews
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import LocationForm, ItemForm, MonsterForm, CommentForm
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView


# class LocationsView(ListView):
#     model = Location
#     queryset = Location.objects.all()


# class LocationDetailView(DetailView):
#     model = Location
#     template_name = 'items/location_detail.html'
#     slug_url_kwargs = 'slug'
#     context_object_name = 'location_detail'
#     slug_field = "url"




class LocationsView(views.View):

    def get(self, request, *args, **kwargs):
        locations = Location.objects.all()
        monsters = Monster.objects.all()
        context = {'locations': locations, 'monsters': monsters}
        return render(request, 'items/index.html', context)


def location_detail(request, slug):
    slug = Location.objects.get(url=slug)
    if slug:
        monsters = Monster.objects.filter(locations=slug)
    else:
        monsters = Monster.objects.all()
    locations = Location.objects.all()
    context = {'monsters': monsters, 'location_detail': locations}
    return render(request, 'items/location_detail.html', context)



def monster_detail(request, slug):
    slug = Monster.objects.get(url=slug)
    print('!!!!!', slug)
    if slug:
        items = Item.objects.filter(monster=slug)
    else:
        items = Item.objects.all()
    monsters = Monster.objects.all()
    context = {'items': items, 'monsters': monsters}
    return render(request, 'items/monster_detail.html', context)




def get_comment(request):
    slug = Monster.objects.all()
    if slug:
        items = Item.objects.filter(monster=slug)
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(request.path_info)

        else:
            form = CommentForm()
            names = Reviews.objects.all()
    else:
        items = Item.objects.all()
    monsters = Monster.objects.all()
    comments = Reviews.objects.all()
    return render(request, 'items/name.html', {
        'form': form,
        'names': names,
        'monsters': monsters,
        'items': items,
        'comments': comments
    })


# class MonsterView(ListView):
#     model = Monster
#     queryset = Monster.objects.all()


# class MonsterDetailView(DetailView):
#     model = Monster
#     slug_field = "url"


# class ItemView(ListView):
#     model = Item
#     queryset = Item.objects.all()
#     print('!!!!!', queryset)


# class ItemDetailView(DetailView):
#     model = Item
#     slug_field = "url"




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
        return redirect('locations')


@login_required
def createlocation(request):
    if request.method == 'GET':
        return render(request, 'items/createlocation.html',
                      {'form': LocationForm()})
    else:
        try:
            form = LocationForm(request.POST,
                                request.FILES,
                                instance=request.user)
            newlocaltion = form.save(commit=False)
            newlocaltion.user = request.user
            newlocaltion.save()
            print('fff ', form)
            print('newlocaltion ', newlocaltion)
            return redirect('locations')
        except ValueError:
            return render(request, 'items/createlocation.html', {
                'form': LocationForm(),
                'error': 'Bad data passed in'
            })


@login_required
def createitem(request):
    if request.method == 'GET':
        return render(request, 'items/createitem.html', {'form': ItemForm()})
    else:
        try:
            form = ItemForm(request.POST, request.FILES, instance=request.user)
            newitem = form.save(commit=False)
            newitem.user = request.user
            newitem.save()
            return redirect('locations')
        except ValueError:
            return render(request, 'items/createitem.html', {
                'form': ItemForm(),
                'error': 'Bad data passed in'
            })


@login_required
def createmonster(request):
    if request.method == 'GET':
        return render(request, 'items/createmonster.html',
                      {'form': MonsterForm()})
    else:
        try:
            form = MonsterForm(request.POST,
                               request.FILES,
                               instance=request.user)
            newmonster = form.save(commit=False)
            newmonster.user = request.user
            newmonster.save()
            return redirect('locations')
        except ValueError:
            return render(request, 'items/createmonster.html', {
                'form': MonsterForm(),
                'error': 'Bad data passed in'
            })


def get_comment(request):
    slug = Monster.objects.all()
    if slug:
        items = Item.objects.filter(monster=slug)
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(request.path_info)

        else:
            form = CommentForm()
            names = Reviews.objects.all()
    else:
        items = Item.objects.all()
    monsters = Monster.objects.all()
    comments = Reviews.objects.all()
    return render(request, 'items/name.html', {
        'form': form,
        'names': names,
        'monsters': monsters,
        'items': items,
        'comments': comments
    })



# def get_items(request, slug):
#     slug = Monster.objects.get(slug=slug)
#     if slug:
#         items = Item.objects.filter(monster=slug)
#     else:
#         items = Item.objects.all()
#     monsters = Monster.objects.all()
#     context = {'items': items, 'monsters': monsters}
#     return render(request, 'items/monsters.html', context)
