"""Contains the application’s url."""
from django.urls import path
from . import views

app_name = 'substitute'

urlpatterns = [
    path('substitute/<int:product_id>', views.substitute, name='search-a-substitute'),
    path('substitute/<int:product_id>/?page=<int:page>', views.substitute, name='search-a-substitute'),
    path('detail/<int:product_id>/<int:substitute_id>/', views.detail, name='detail'),
    path('save/<int:product_id>/<int:substitute_id>/', views.save, name='save'),
    path('detail_favoris/<int:product_id>/<int:substitute_id>/', views.detail_favoris, name='detail_favoris'),
]