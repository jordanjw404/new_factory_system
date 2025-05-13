<<<<<<< HEAD
<<<<<<< HEAD
from django.urls import path
from .views import inventory_list_view
=======
from django.urls import path, include
from django.conf.urls.static import static
from . import views
from django.conf import settings
from django.contrib import admin
>>>>>>> b56bbc1 (Refactor inventory URLs and views; add specific views for cabinets, boards, hardware, and edge banding)
=======
from django.urls import path
from .views import inventory_list_view
>>>>>>> d92dd45 (Implement inventory list view and template; add slug fields to models for better URL handling)

app_name = 'inventory'

urlpatterns = [
<<<<<<< HEAD
<<<<<<< HEAD
    path('', inventory_list_view, name='inventory_list'),
=======
    path('', views.inventory_list, name='inventory_list'),
    path('cabinets/', views.cabinet_list, name='cabinet_list'),
    path('boards/', views.board_list, name='board_list'),
    path('hardware/', views.hardware_list, name='hardware_list'),
    path('edgebanding/', views.edgebanding_list, name='edgebanding_list'),
>>>>>>> b56bbc1 (Refactor inventory URLs and views; add specific views for cabinets, boards, hardware, and edge banding)
=======
    path('', inventory_list_view, name='inventory_list'),
>>>>>>> d92dd45 (Implement inventory list view and template; add slug fields to models for better URL handling)
]
