from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.LocationsView.as_view(), name="locations"),
    path('monsters/', views.FilterMonstersView.as_view(), name="monsters"),
    # path('monsters/', views.MonstersView.as_view(), name="monsters"),
    path('items/<str:slug>/', views.ItemsView.as_view(), name="item"),
    # path('location/<str:slug>/',
    #      views.MonstersView.as_view(),
    #      name='location'),
    path('location/<int:id>/',
         views.get_local,
         name='monsters'),
    # path("<str:slug>/", views.ItemDetailView.as_view(), name="item_detail"),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
