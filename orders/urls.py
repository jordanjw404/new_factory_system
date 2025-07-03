from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('create/', views.order_create, name='order_create'),
    path('<int:pk>/', views.order_detail, name='order_detail'),
    path('<int:pk>/edit/', views.order_edit, name='order_edit'),
    path('<int:pk>/delivery-update/', views.delivery_date_update, name='delivery_date_update'),
    path('<int:pk>/delete/', views.order_delete, name='order_delete'),
    path('detail-list/', views.order_detail_list, name='order_detail_list'),
    path('export/excel/', views.export_orders_excel, name='export_orders_excel'),
]