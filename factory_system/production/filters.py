import django_filters
from .models import ProductionStage
from django import forms

class ProductionStageFilter(django_filters.FilterSet):
    sales_status = django_filters.ChoiceFilter(
        choices=ProductionStage.SALES_STATUS,  # Corrected here
        label="Sales",
        widget=forms.Select(attrs={"class": "form-select form-select-sm"})
    )
    programming_status = django_filters.ChoiceFilter(
        choices=ProductionStage.STAGE_STATUS,  # Corrected here
        label="Programming",
        widget=forms.Select(attrs={"class": "form-select form-select-sm"})
    )
    nest_status = django_filters.ChoiceFilter(
        choices=ProductionStage.STAGE_STATUS,  # Corrected here
        label="Nest",
        widget=forms.Select(attrs={"class": "form-select form-select-sm"})
    )
    build_status = django_filters.ChoiceFilter(
        choices=ProductionStage.STAGE_STATUS,  # Corrected here
        label="Build",
        widget=forms.Select(attrs={"class": "form-select form-select-sm"})
    )
    
    class Meta:
        model = ProductionStage
        fields = ['sales_status', 'programming_status', 'nest_status', 'build_status']
