from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.LocationsView.as_view(), name="locations"),
    path('monsters/<str:slug>/',
         views.get_items,
         name='monsters'),
    path('location/<str:slug>/',
         views.get_local,
         name='locations'),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
