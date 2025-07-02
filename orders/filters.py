import django_filters
from django import forms
from django_filters import widgets

from customers.models import Customer

from .models import Order


class OrderFilter(django_filters.FilterSet):
    customer = django_filters.ModelChoiceFilter(
        queryset=Customer.objects.all(),
        label="Customer",
        widget=forms.Select(attrs={"class": "form-select form-select-sm"}),
    )

    reference = django_filters.CharFilter(
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"class": "form-control form-control-sm"}),
    )

    status = django_filters.ChoiceFilter(
        choices=Order.Status.choices,
        widget=forms.Select(attrs={"class": "form-select form-select-sm"}),
    )

    order_type = django_filters.ChoiceFilter(
        choices=Order.OrderType.choices,
        widget=forms.Select(attrs={"class": "form-select form-select-sm"}),
    )

    priority = django_filters.ChoiceFilter(
        choices=Order.Priority.choices,
        widget=forms.Select(attrs={"class": "form-select form-select-sm"}),
    )

    delivery_date = django_filters.DateFromToRangeFilter(
        label="Delivery Date",
        widget=widgets.RangeWidget(
            attrs={"type": "date", "class": "form-control form-control-sm"}
        ),
    )

    class Meta:
        model = Order
        fields = [
            "customer",
            "reference",
            "status",
            "order_type",
            "priority",
            "delivery_date",
        ]
