from django.urls import path
from .views import create_customer_view
from . import views
app_name = 'customers'

urlpatterns = [
    path("add/", create_customer_view, name="customer-add"),
    path('<int:pk>/', views.customer_detail, name='customer_detail'),
]
