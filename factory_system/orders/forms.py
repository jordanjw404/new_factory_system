from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'name', 'customer', 'reference', 'delivery_date', 'is_collection',
            'order_type', 'status', 'robes', 'cabs', 'panels', 'owner'
        ]
        widgets = {
            'delivery_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column("name", css_class="col-md-6"),
                Column("reference", css_class="col-md-6"),
            ),
            Row(
                Column("customer", css_class="col-md-6"),
                Column("owner", css_class="col-md-6"),
            ),
            Row(
                Column("delivery_date", css_class="col-md-6"),
                Column("is_collection", css_class="col-md-6"),
            ),
            Row(
                Column("order_type", css_class="col-md-6"),
                Column("status", css_class="col-md-6"),
            ),
            Row(
                Column("robes", css_class="col-md-4"),
                Column("cabs", css_class="col-md-4"),
                Column("panels", css_class="col-md-4"),
            ),
            Submit("submit", "Save Order", css_class="btn btn-primary w-100 mt-3")
        )
