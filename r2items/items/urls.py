from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'item'

urlpatterns = [
    path('', views.LocationsView.as_view(), name="locations"),
    path('signup/', views.signupuser, name='signupuser'),
    path('logout/', views.logoutuser,  name="logoutuser"),
    path('login/', views.loginuser,  name="loginuser"),
    path('create/', views.createlocation, name='createlocation'),
    path('createitem/', views.createitem, name='createitem'),
    path('createmonster/', views.createmonster, name='createmonster'),
    # path('monsters/<str:slug>/',
    #      views.get_items,
    #      name='monsters'),
    path('monsters/<str:slug>/',
         views.get_comment,
         name='names'),
    path('location/<str:slug>/',
         views.get_local,
         name='locations'),
   
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
