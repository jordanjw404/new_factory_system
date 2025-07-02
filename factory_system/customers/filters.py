import django_filters

from .models import Customer


class CustomerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains", label="Search Name")

    class Meta:
        model = Customer
        fields = ["name"]
