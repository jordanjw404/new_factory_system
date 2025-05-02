from django.urls import path
from . import views
from .views import export_inventory_csv, add_stock_item, import_inventory
from django.http import HttpResponse
urlpatterns = [
    path('stock-in/', views.stock_in, name='stock-in'),
    path('stock-out/', views.stock_out, name='stock-out'),
    path('stock-transfer/', views.stock_transfer, name='stock-transfer'),
    path('list/', views.inventory_list, name='inventory-list'),
    path('item/<int:pk>/', views.inventory_detail, name='inventory-detail'),
    path('movements/', views.movement_log, name='movement-log'),
    path('incoming/create/', views.create_incoming_order, name='incoming-order-create'),
    path('incoming/', views.incoming_order_list, name='incoming-order-list'),
    path('incoming/<int:pk>/', views.incoming_order_detail, name='incoming-order-detail'),
    path('inventory/export/', export_inventory_csv, name='inventory-export'),
    path('add/', add_stock_item, name='add-stock-item'),
    path('import/', import_inventory, name='import-inventory'),
    path('import/', export_inventory_csv, name='export-inventory'),
]


def import_inventory(request):
    return HttpResponse("Import view coming soon.")
