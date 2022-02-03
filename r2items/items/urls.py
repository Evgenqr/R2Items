from unicodedata import name
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.LocationsView.as_view(), name="locations"),
    path('items/', views.ItemsView.as_view(), name="items"),
    path('monsters/', views.MonstersView.as_view(), name="monsters"),
    path("<str:slug>/", views.ItemDetailView.as_view(), name="item_detail"),

]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
