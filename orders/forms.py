from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Field, Layout, Row, Submit
from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "name",
            "customer",
            "reference",
            "delivery_date",
            "is_collection",
            "order_type",
            "priority",
            "status",
            "robes",
            "cabs",
            "panels",
            "owner",
            "send_to_production",
        ]
        widgets = {
            "delivery_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.label_class = "form-label"
        self.helper.field_class = "form-control"

        self.helper.layout = Layout(
            Row(
                Column(FloatingField("name", css_class="mb-3")),
                Column(FloatingField("customer", css_class="mb-3")),
            ),
            FloatingField("reference"),
            Row(
                Column(FloatingField("delivery_date", css_class="mb-3")),
                Column(Field("is_collection", css_class="form-check-input me-5 mb-3")),
            ),
            Row(
                Column(FloatingField("order_type")),
                Column(FloatingField("priority")),
                Column(FloatingField("status")),
            ),
            Row(
                Column(FloatingField("robes")),
                Column(FloatingField("cabs")),
                Column(FloatingField("panels")),
            ),
            Field("send_to_production", css_class="form-check-input me-5 mb-3"),
            FloatingField("owner"),
            Submit("submit", "Save Order", css_class="btn btn-success w-100 mt-3"),
        )
