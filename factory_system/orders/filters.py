import django_filters
from .models import Order
from django import forms
from customers.models import Customer

class OrderFilter(django_filters.FilterSet):
    customer = django_filters.ModelChoiceFilter(
        queryset=Customer.objects.all(),
        label="Customer",
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
    )
    reference = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'})
    )
    status = django_filters.ChoiceFilter(
        choices=Order.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
    )
    order_type = django_filters.ChoiceFilter(
        choices=Order.ORDER_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
    )
