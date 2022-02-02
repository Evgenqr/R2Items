from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.BaseView),
    path("<str:slug>/", views.ItemDetailView.as_view(), name="item_detail"),
]
