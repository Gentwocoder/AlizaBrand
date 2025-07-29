from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('collections/', views.collections, name='collections'),
    path('contact/', views.contact, name='contact'),
]
