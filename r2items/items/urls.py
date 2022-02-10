from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.LocationsView.as_view(), name="location_list"),  # location_list
    path("location/<slug:slug>/", views.MonsterView.as_view(), name="location_list"),  # monster_list ???
    path("monster/<slug:slug>/", views.ItemView.as_view(), name="item_list"), # monster_detail
    path("item/<slug:slug>/", views.ItemView.as_view(), name="item_list"),
    path('signup/', views.signupuser, name='signupuser'),
    path('logout/', views.logoutuser,  name="logoutuser"),
    path('login/', views.loginuser,  name="loginuser"),
    path('create/', views.createlocation, name='createlocation'),
    path('createitem/', views.createitem, name='createitem'),
    path('createmonster/', views.createmonster, name='createmonster'),

    

    # path('monsters/<str:slug>/',
    #      views.get_items,
    #      name='monsters'),
    # path('monsters/<str:slug>/',
    #      views.get_comment,
    #      name='names'),
    # path('location/<int:pk>/',
    #      views.get_local,
    #      name='locations'),
   
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
