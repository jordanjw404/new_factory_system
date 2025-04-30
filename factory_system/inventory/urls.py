from django.urls import path
from . import views

urlpatterns = [
    path('stock-in/', views.stock_in, name='stock-in'),
    path('stock-out/', views.stock_out, name='stock-out'),
    path('stock-transfer/', views.stock_transfer, name='stock-transfer'),
    
]
