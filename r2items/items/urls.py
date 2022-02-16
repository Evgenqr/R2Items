from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.LocationsView.as_view(), name="home"),
    path('location/<str:slug>/', views.location_detail, name='location_detail'),
    path('location/<str:slug>/newmonster/', views.createmonster, name='createmonster'),
    path('monster/<str:slug>/', views.monster_detail, name='monster_detail'),
    path('signup/', views.signupuser, name='signupuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('login/', views.loginuser,  name="loginuser"),
    path('create/', views.createlocation, name='createlocation'),
    # path('createitem/', views.createitem, name='createitem'),
    path('monster/<str:slug>/newitem/', views.createmonster, name='createmonster'),
    # path('createmonster/', views.createmonster, name='createmonster'),
    path('location/<str:slug>/view/', views.viewlocation, name='viewlocation'),
    path('location/<str:slug>/delete', views.deletelocation, name='deletelocation'),
    path('monster/<str:slug>/view/', views.viewmonster, name='viewmonster'),
    path('monster/<str:slug>/delete', views.deletemonster, name='deletemonster'),
    # path('monsters/<str:url>/',
    #      views.get_comment,
    #      name='names'),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
