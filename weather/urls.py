from django.urls import path
from . import views

app_name = 'weather'

urlpatterns = [
    # Home Page.
    path('', views.index, name='index'),
    # Search Page
    path('search/', views.search, name='search'),
    # Url for Delete.
    path('delete/<city_name>/', views.delete_city, name='delete_city'),
    # Url for clearing all cities.
    path('deleteall/', views.delete_everything, name='delete_everything'),
]