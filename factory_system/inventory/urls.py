from django.urls import path
from .views import inventory_list_view

app_name = 'inventory'

urlpatterns = [
    path('', inventory_list_view, name='inventory_list'),
]
