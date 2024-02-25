from django.contrib import admin
from django.urls import path, include

from .views import index, add_inventory, display_inventory,generate_pdf, gemini, ulogin, dashboard

urlpatterns = [
    path('', index, name='index'),
    path('add_inventory', add_inventory, name='add_inventory'),
    path('display_inventory', display_inventory, name='display_inventory'),

    path('ulogin', ulogin, name='ulogin'),
    path('dashboard', dashboard, name='dashboard'),

    path('generate_pdf', generate_pdf, name='generate_pdf'),
    path('gemini', gemini, name='gemini'),


]