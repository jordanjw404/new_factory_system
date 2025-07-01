from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('kpi-dashboard/', views.factory_kpi_dashboard, name='factory_kpi_dashboard'),
]
