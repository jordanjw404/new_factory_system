from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row, Submit
from django import forms

from .models import ProductionStage


class ProductionStageForm(forms.ModelForm):
    class Meta:
        model = ProductionStage
        fields = [
            "order",  # Required to assign the order
            "sales_status",
            "programming_status",
            "nest_status",
            "edge_status",
            "prep_status",
            "build_status",
            "fittings_status",
            "wrapping_status",
            "quality_status",
            "sales_target_date",
            "programming_target_date",
            "nest_target_date",
            "edge_target_date",
            "prep_target_date",
            "build_target_date",
            "fittings_target_date",
            "wrapping_target_date",
            "quality_target_date",
            "sales_completed_date",
            "programming_completed_date",
            "nest_completed_date",
            "edge_completed_date",
            "prep_completed_date",
            "build_completed_date",
            "fittings_completed_date",
            "wrapping_completed_date",
            "quality_completed_date",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.label_class = "form-label"
        self.helper.field_class = "form-control"

        self.helper.layout = Layout(
            Row(
                Column(FloatingField("order")),
            ),
            Row(
                Column(FloatingField("sales_status")),
                Column(FloatingField("sales_target_date")),
                Column(FloatingField("sales_completed_date")),
            ),
            Row(
                Column(FloatingField("programming_status")),
                Column(FloatingField("programming_target_date")),
                Column(FloatingField("programming_completed_date")),
            ),
            Row(
                Column(FloatingField("nest_status")),
                Column(FloatingField("nest_target_date")),
                Column(FloatingField("nest_completed_date")),
            ),
            Row(
                Column(FloatingField("edge_status")),
                Column(FloatingField("edge_target_date")),
                Column(FloatingField("edge_completed_date")),
            ),
            Row(
                Column(FloatingField("prep_status")),
                Column(FloatingField("prep_target_date")),
                Column(FloatingField("prep_completed_date")),
            ),
            Row(
                Column(FloatingField("build_status")),
                Column(FloatingField("build_target_date")),
                Column(FloatingField("build_completed_date")),
            ),
            Row(
                Column(FloatingField("fittings_status")),
                Column(FloatingField("fittings_target_date")),
                Column(FloatingField("fittings_completed_date")),
            ),
            Row(
                Column(FloatingField("wrapping_status")),
                Column(FloatingField("wrapping_target_date")),
                Column(FloatingField("wrapping_completed_date")),
            ),
            Row(
                Column(FloatingField("quality_status")),
                Column(FloatingField("quality_target_date")),
                Column(FloatingField("quality_completed_date")),
            ),
        )
