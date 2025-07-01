from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('', views.customer_list, name='customer_list'),
    path('details/', views.customer_detail_list, name='customer_detail_list'),
    path('create/', views.customer_create, name='customer_create'),
    path('<int:pk>/', views.customer_detail, name='customer_detail'),
    path('<int:pk>/edit/', views.customer_edit, name='customer_edit'),
    path('<int:pk>/delete/', views.customer_delete, name='customer_delete'),
    path('export/', views.export_customers_csv, name='export_customers'),
    path('import/', views.import_customers_csv, name='import_customers'),
    path('<int:customer_pk>/documents/<int:doc_pk>/delete/', views.delete_customer_document, name='customer_document_delete'),

]
