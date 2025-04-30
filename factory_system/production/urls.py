from django.urls import path
from . import views

app_name = 'production'

urlpatterns = [
    path('', views.production_list, name='production_list'),
    path('create/', views.production_create, name='production_create'),
    path('<int:pk>/', views.production_detail, name='production_detail'),
    path('<int:pk>/edit/', views.production_edit, name='production_edit'),
    path('<int:pk>/delete/', views.production_delete, name='production_delete'),
    path('<int:pk>/update_status/', views.production_update_status, name='production_update_status'),
    path('production_export/', views.production_export, name='production_export'),
    path('detail/', views.production_detail_list, name='production_detail_list'),
    path('detail/export/', views.production_detail_export, name='production_detail_export'),

]
