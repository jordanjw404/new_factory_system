from django.urls import path
from . import views

app_name = "inventory"

urlpatterns = [
    path("stock/", views.product_list, name="stock_list"),
    path("product/<uuid:product_id>/action/", views.product_action_view, name="product_action"),
    path("transactions/", views.stock_txn_list, name="stock_txn_list"),
]
