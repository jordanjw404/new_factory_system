import django_filters
from .models import Order
from django import forms
from customers.models import Customer

class OrderFilter(django_filters.FilterSet):
    customer = django_filters.ModelChoiceFilter(
        queryset=Customer.objects.all(),
        label="Customer"
    )
    reference = django_filters.CharFilter(lookup_expr='icontains')
    status = django_filters.ChoiceFilter(choices=Order.STATUS_CHOICES)
    order_type = django_filters.ChoiceFilter(choices=Order.ORDER_TYPE_CHOICES)

    class Meta:
        model = Order
        fields = ['customer', 'reference', 'status', 'order_type']
