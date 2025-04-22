from django.urls import path
from .views import create_customer_view

urlpatterns = [
    path("add/", create_customer_view, name="customer-add"),
]
