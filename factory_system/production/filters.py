import django_filters
from django import forms

from .models import ProductionStage


class ProductionStageFilter(django_filters.FilterSet):
    sales_status = django_filters.ChoiceFilter(
        choices=ProductionStage.SALES_STATUS,
        label="Sales",
        widget=forms.Select(attrs={"class": "form-select form-select-sm"}),
    )
    programming_status = django_filters.ChoiceFilter(
        choices=ProductionStage.STAGE_STATUS,
        label="Programming",
        widget=forms.Select(attrs={"class": "form-select form-select-sm"}),
    )
    nest_status = django_filters.ChoiceFilter(
        choices=ProductionStage.STAGE_STATUS,
        label="Nest",
        widget=forms.Select(attrs={"class": "form-select form-select-sm"}),
    )
    edge_status = django_filters.ChoiceFilter(
        choices=ProductionStage.STAGE_STATUS,
        label="Edge",
        widget=forms.Select(attrs={"class": "form-select form-select-sm"}),
    )
    prep_status = django_filters.ChoiceFilter(
        choices=ProductionStage.STAGE_STATUS,
        label="Prep",
        widget=forms.Select(attrs={"class": "form-select form-select-sm"}),
    )
    build_status = django_filters.ChoiceFilter(
        choices=ProductionStage.STAGE_STATUS,
        label="Build",
        widget=forms.Select(attrs={"class": "form-select form-select-sm"}),
    )
    fittings_status = django_filters.ChoiceFilter(
        choices=ProductionStage.STAGE_STATUS,
        label="Fittings",
        widget=forms.Select(attrs={"class": "form-select form-select-sm"}),
    )
    wrapping_status = django_filters.ChoiceFilter(
        choices=ProductionStage.STAGE_STATUS,
        label="Wrapping",
        widget=forms.Select(attrs={"class": "form-select form-select-sm"}),
    )
    quality_status = django_filters.ChoiceFilter(
        choices=ProductionStage.STAGE_STATUS,
        label="Quality",
        widget=forms.Select(attrs={"class": "form-select form-select-sm"}),
    )

    class Meta:
        model = ProductionStage
        fields = [
            "sales_status",
            "programming_status",
            "nest_status",
            "edge_status",
            "prep_status",
            "build_status",
            "fittings_status",
            "wrapping_status",
            "quality_status",
        ]
