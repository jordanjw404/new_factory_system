from django.urls import path
from .views import StockInView, StockOutView, TransferView, AddItemView, BoardStockCreateView

app_name = 'inventory'

urlpatterns = [
    path('stock-in/', StockInView.as_view(), name='stock_in'),
    path('stock-out/', StockOutView.as_view(), name='stock_out'),
    path('transfer/', TransferView.as_view(), name='transfer'),
    path('add-item/', AddItemView.as_view(), name='add_item'),
    path('add-board-stock/', BoardStockCreateView.as_view(), name='add_board_stock'),
]
