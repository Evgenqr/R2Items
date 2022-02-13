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


class LocationsView(views.View):
    def get(self, request, *args, **kwargs):
        locations = Location.objects.all()
        monsters = Monster.objects.all()
        context = {'locations': locations, 'monsters': monsters}
        return render(request, 'items/index.html', context)


@login_required
def location_detail(request, slug):
    slug = Location.objects.get(url=slug)
    locations = Location.objects.all()
    if slug:
        monsters = Monster.objects.filter(locations=slug)
    else:
        monsters = Monster.objects.all()
    context = {'monsters': monsters, 'locations': locations}
    return render(request, 'items/location_detail.html', context)


@login_required
def monster_detail(request, slug):
    slug = Monster.objects.get(url=slug)
    locations = Location.objects.all()
    print('!!!!!', slug)
    if slug:
        items = Item.objects.filter(monster=slug)
    else:
        items = Item.objects.all()
    monsters = Monster.objects.all()
    context = {'items': items, 'monsters': monsters, 'locations': locations}
    return render(request, 'items/monster_detail.html', context)



# @login_required
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


@login_required
def createlocation(request):
    print('11??????????22')
    if request.method == 'GET':
        print('??????????')
        return render(request, 'items/createlocation.html',
                      {'form': LocationForm()})
    else:
        try:
            form = LocationForm(request.POST,
                                request.FILES)
            newlocaltion = form.save(commit=False)
            print('!!!', newlocaltion)
            newlocaltion.user = request.user
            print('1111', newlocaltion)
            newlocaltion.save()
            return redirect('home')
        except ValueError:
            return render(request, 'items/createlocation.html', {
                'form': LocationForm(),
                'error': 'Bad data passed in'
            })


def viewlocation(request, slug):
    location = get_object_or_404(Location, url=slug)
    if request.method == 'GET':
        form = LocationForm(instance=location)
        return render(request, 'items/veiwlocation.html', {'location': location, 'form': form})
    else:
        try:
            form = LocationForm(request.POST, instance=location)
            form.save()
            return redirect('home')
        except ValueError:
            return render(request, 'items/veiwlocation.html', {
                'todo': location,
                'form': LocationForm(),
                'error': 'Bad info'
            })


@login_required
def deletelocation(request, slug):
    location = get_object_or_404(Location, url=slug)
    if request.method == 'POST':
        location.delete()
        return redirect('home')


@login_required
def createitem(request):
    if request.method == 'GET':
        return render(request, 'items/createitem.html', {'form': ItemForm()})
    else:
        try:
            form = ItemForm(request.POST, request.FILES)
            newitem = form.save(commit=False)
            newitem.user = request.user
            newitem.save()
            return redirect('home')
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
            form = MonsterForm(request.POST, request.FILES)
            newmonster = form.save(commit=False)
            newmonster.user = request.user
            newmonster.save()
            return redirect('home')
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
