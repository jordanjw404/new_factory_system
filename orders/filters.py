import django_filters
from django import forms
from django_filters import widgets

from customers.models import Customer
from production.models import ProductionStage

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

    # ——— NEW: current_stage filter ———
    CURRENT_STAGE_CHOICES = [
        ('all',   'All'),
        ('nest',  'Nest'),
        ('build', 'Build'),
        ('prep',  'Prep'),
    ]
    current_stage = django_filters.ChoiceFilter(
        label="Stage",
        choices=CURRENT_STAGE_CHOICES,
        method='filter_current_stage',
        widget=forms.Select(attrs={"class": "form-select form-select-sm"})
    )

    def filter_current_stage(self, queryset, name, value):
        # “All” or blank = no filtering
        if not value or value == 'all':
            return queryset
        # Map the stage key to a non-null lookup on the related ProductionStage
        lookup = {
            'nest':  'productionstage__nest_status__isnull=False',
            'build': 'productionstage__build_status__isnull=False',
            'prep':  'productionstage__prep_status__isnull=False',
        }
        return queryset.filter(**{lookup[value]: True})

    class Meta:
        model = Order
        fields = [
            "customer",
            "reference",
            "status",
            "order_type",
            "priority",
            "delivery_date",
            "current_stage",
        ]
