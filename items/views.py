from django.shortcuts import redirect, render, get_object_or_404
from .models import Item, Location, Monster, Category
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import LocationForm, ItemForm, MonsterForm, CategoryForm
from django.views.generic import ListView, DetailView
from django.utils.text import slugify
from transliterate import translit
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from itertools import chain


# ---- Location
class LocationsView(ListView):

    model = Location
    template_name = 'items/index.html'
    context_object_name = 'locations'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Главная страница'
        return context


@login_required
def createlocation(request):
    if request.method == 'GET':
        return render(request, 'items/createlocation.html',
                      {'form': LocationForm()})
    else:
        try:
            form = LocationForm(request.POST, request.FILES)
            newlocaltion = form.save(commit=False)
            newlocaltion.user = request.user
            newlocaltion.slug = translit(newlocaltion.name,
                                         language_code='ru',
                                         reversed=True)
            newlocaltion.slug = slugify(newlocaltion.slug)
            newlocaltion.save()
            return redirect('home')
        except ValueError:
            return render(request, 'items/createlocation.html', {
                'form': LocationForm(),
                'error': 'Bad data passed in'
            })


@login_required
def viewlocation(request, slug):
    location = get_object_or_404(Location, slug=slug)
    if location.user == request.user or request.user.has_perm('auth.change_user'):
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
        return redirect('/')


@login_required
def deletelocation(request, slug):
    if location.user == request.user:
        location = get_object_or_404(Location, slug=slug)
        if request.method == 'POST':
            location.delete()
            return redirect('home')
    else:
        return redirect('/')
# ---- Location END

# ---- Monster


class MonstersInLocation(ListView):
    model = Monster
    template_name = 'items/location_detail.html'
    context_object_name = 'monsters'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = Location.objects.get(slug=self.kwargs['slug'])
        return context

    def get_queryset(self):
        slug = Location.objects.get(slug=self.kwargs['slug'])
        if slug:
            return Monster.objects.filter(locations=slug)


@login_required
def createmonster(request):
    if request.method == 'POST':
        form = MonsterForm(request.POST, request.FILES)
        if form.is_valid():
            locations = form.cleaned_data.get("locations")
            newmonster = form.save(commit=False)
            newmonster.user = request.user
            newmonster.slug = translit(newmonster.name,
                                       language_code='ru',
                                       reversed=True)
            newmonster.slug = slugify(newmonster.slug)
            newmonster.save()
            for local in locations:
                newmonster.locations.add(local)
            return redirect('home')
    else:
        form = MonsterForm()
    return render(request, 'items/createmonster.html', {'form': form})


@login_required
def viewmonster(request, slug):
    monster = get_object_or_404(Monster, slug=slug)
    if monster.user == request.user or request.user.has_perm('auth.change_user'):
        if request.method == 'GET':
            form = MonsterForm(instance=monster)
            return render(request, 'items/viewmonster.html', {
                'monster': monster,
                'form': form
            })
        else:
            try:
                form = MonsterForm(
                    request.POST, request.FILES, instance=monster)
                form.save()
                return redirect('home')
            except ValueError:
                return render(request, 'items/viewmonster.html', {
                    'monster': monster,
                    'form': MonsterForm(),
                    'error': 'Bad info'
                })
    else:
        return redirect('/')


@login_required
def deletemonster(request, slug):
    monster = get_object_or_404(Monster, slug=slug)
    if monster.user == request.user or request.user.has_perm('auth.change_user'):
        if request.method == 'POST':
            monster.delete()
            return redirect('home')
    else:
        return redirect('/')
# ---- Monster END

# ---- Item


class ItemInMonster(ListView):
    model = Item
    template_name = 'items/monster_detail.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = Monster.objects.get(slug=self.kwargs['slug'])
        return context

    def get_queryset(self):
        slug = Monster.objects.get(slug=self.kwargs['slug'])
        if slug:
            return Item.objects.filter(monster=slug)


class ItemDetail(DetailView):
    model = Item
    template_name = 'items/item_detail.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = Item.objects.get(slug=self.kwargs['slug'])
        return context


@login_required
def createitem(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            monster = form.cleaned_data.get('monster')
            newitem = form.save(commit=False)
            newitem.user = request.user
            newitem.slug = translit(newitem.name,
                                    language_code='ru',
                                    reversed=True)
            newitem.slug = slugify(newitem.slug)
            newitem.save()
            for mob in monster:
                newitem.monster.add(mob)
            return redirect('home')
    else:
        form = ItemForm()
    return render(request, 'items/createitem.html', {'form': form})


@login_required
def viewitem(request, slug):
    item = get_object_or_404(Item, slug=slug)
    if item.user == request.user or request.user.has_perm('auth.change_user'):
        if request.method == 'GET':
            form = ItemForm(instance=item)
            return render(request, 'items/viewitem.html', {
                'item': item,
                'form': form
            })
        else:
            try:
                form = ItemForm(request.POST, request.FILES, instance=item)
                form.save()
                return redirect('home')
            except ValueError:
                return render(request, 'items/viewitem.html', {
                    'item': item,
                    'form': ItemForm(),
                    'error': 'Bad info'
                })
    else:
        return redirect('/')


@login_required
def deleteitem(request, slug):
    item = get_object_or_404(Item, slug=slug)
    if item.user == request.user or request.user.has_perm('auth.change_user'):
        if request.method == 'POST':
            item.delete()
            return redirect('home')
    else:
        return redirect('/')
# ---- Item END


# ---- Category
@login_required
def createcategory(request):
    if request.method == 'GET':
        return render(request, 'items/createcategory.html',
                      {'form': CategoryForm()})
    else:
        try:
            form = CategoryForm(request.POST, request.FILES)
            newcategory = form.save(commit=False)
            # newlocaltion.slug = request.user
            newcategory.user = request.user
            newcategory.slug = translit(newcategory.name,
                                        language_code='ru',
                                        reversed=True)
            newcategory.slug = slugify(newcategory.slug)
            newcategory.save()
            return redirect('home')
        except ValueError:
            return render(request, 'items/createcategory.html', {
                'form': CategoryForm(),
                'error': 'Bad data passed in'
            })


@login_required
def viewcategory(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if category.user == request.user or request.user.has_perm('auth.change_user'):
        if request.method == 'GET':
            form = CategoryForm(instance=category)
            return render(request, 'items/viewcategory.html', {
                'category': category,
                'form': form
            })
        else:
            try:
                form = CategoryForm(request.POST,
                                    request.FILES,
                                    instance=category)
                form.save()
                return redirect('home')
            except ValueError:
                return render(
                    request, 'items/viewlocation.html', {
                        'category': category,
                        'form': CategoryForm(),
                        'error': 'Bad info'
                    })
    else:
        return redirect('/')


@login_required
def deletecategory(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if category.user == request.user or request.user.has_perm('auth.change_user'):
        if request.method == 'POST':
            category.delete()
            return redirect('/')
    return redirect('/')
# ---- Category END


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


class SearchView(ListView):
    template_name = 'items/search_result.html'

    def get(self, request, *args, **kwargs):
        context = {}
        q = request.GET.get('q')
        if q:
            query_sets = []  # Общий QuerySet
            query_sets.append(Location.objects.filter(name__icontains=q))
            query_sets.append(Monster.objects.filter(name__icontains=q))
            query_sets.append(Item.objects.filter(name__icontains=q))
            query_sets.append(Category.objects.filter(name__icontains=q))
            # Ищем по всем моделям
            # и объединяем выдачу
            final_set = list(chain(*query_sets))
            context['last_question'] = '?q=%s' % q
            current_page = Paginator(final_set, 10)
            page = request.GET.get('page')
            try:
                context['object_list'] = current_page.page(page)
            except PageNotAnInteger:
                context['object_list'] = current_page.page(1)
            except EmptyPage:
                context['object_list'] = current_page.page(
                    current_page.num_pages)

        return render(request=request,
                      template_name=self.template_name,
                      context=context
                      )
