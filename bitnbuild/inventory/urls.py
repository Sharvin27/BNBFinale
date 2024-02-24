from django.contrib import admin
from django.urls import path, include
from .views import index, add_inventory, display_inventory, ulogin, dashboard
urlpatterns = [
    path('', index, name='index'),
    path('add_inventory', add_inventory, name='add_inventory'),
    path('display_inventory', display_inventory, name='display_inventory'),
    path('ulogin', ulogin, name='ulogin'),
    path('dashboard', dashboard, name='dashboard'),
]