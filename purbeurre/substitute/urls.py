"""Contains the application’s url."""
from django.urls import path
from . import views

app_name = 'substitute'

urlpatterns = [
    path('', views.home),
    path('substitute', views.substitute, name='search-a-substitute'),
    path('search/', views.search, name='search'),
    path('search-nova/', views.searchnova, name='search-nova'),
    path('product/', views.product, name='product'),
]