from django.urls import path, include
from django.conf.urls.static import static
from . import views
from django.conf import settings
from django.contrib import admin

app_name = 'inventory'

urlpatterns = [
    path('', views.inventory_list, name='inventory_list'),
    path('cabinets/', views.cabinet_list, name='cabinet_list'),
    path('boards/', views.board_list, name='board_list'),
    path('hardware/', views.hardware_list, name='hardware_list'),
    path('edgebanding/', views.edgebanding_list, name='edgebanding_list'),
]
