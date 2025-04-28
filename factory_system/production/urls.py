# production/urls.py
from django.urls import path
from . import views

app_name = 'production'

urlpatterns = [
    path('', views.production_list, name='production_list'),
    path('<int:pk>/', views.production_detail, name='production_detail'),
    path('create/', views.production_create, name='production_create'),
]
