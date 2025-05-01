from django.urls import path
from . import views

urlpatterns = [
    path('stock-in/', views.stock_in, name='stock-in'),
    path('stock-out/', views.stock_out, name='stock-out'),
    path('stock-transfer/', views.stock_transfer, name='stock-transfer'),
    path('list/', views.inventory_list, name='inventory-list'),
    path('item/<int:pk>/', views.inventory_detail, name='inventory-detail'),
    path('movements/', views.movement_log, name='movement-log'),
    path('incoming/create/', views.create_incoming_order, name='incoming-order-create'),

]
