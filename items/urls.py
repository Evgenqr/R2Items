from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.LocationsView.as_view(), name="home"),

    # -----> Location
    path('location/<str:slug>/',
         views.MonstersInLocation.as_view(),
         name='location_detail'),
    path('create/', views.createlocation, name='createlocation'),
    path('location/<str:slug>/view/', views.viewlocation, name='viewlocation'),
    path('location/<str:slug>/delete',
         views.deletelocation,
         name='deletelocation'),
    #  <---- End Location

    # -----> Monster
    path('monster/<str:slug>/',
         views.ItemInMonster.as_view(),
         name='monster_detail'),
    path('newmonster/',
         views.createmonster,
         name='createmonster'),
    path('monster/<str:slug>/view/', views.viewmonster, name='viewmonster'),
    path('monster/<str:slug>/delete',
         views.deletemonster,
         name='deletemonster'),
    #  <---- End Monster

    # -----> Item
    path('item/<str:slug>/',
         views.ItemDetail.as_view(),
         name='item_detail'),
    path('createitem/', views.createitem, name='createitem'),
    path('item/<str:slug>/view/', views.viewitem, name='viewitem'),
    path('item/<str:slug>/delete',
         views.deleteitem,
         name='deleteitem'),
    #  <---- End Item

    # -----> Category
    path('createcategory/', views.createcategory, name='createcategory'),
    path('createcategory/<str:slug>/view/',
         views.viewcategory, name='viewcategory'),
    path('createcategory/<str:slug>/delete',
         views.deletecategory,
         name='deletecategory'),
    #  <---- End Category

    # -----> For User
    path('signup/', views.signupuser, name='signupuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('login/', views.loginuser, name="loginuser"),
    #  <---- End For User
    path('search/', views.SearchView.as_view(), name='search'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
