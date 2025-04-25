from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("", views.order_list, name="order_list"),
    path("<int:pk>/", views.order_detail, name="order_detail"),
    path("create/", views.order_create, name="order_create"),
    path("details/", views.order_detail_list, name="order_detail_list"),
    path('export/', views.export_orders_excel, name='order_export'),

]
