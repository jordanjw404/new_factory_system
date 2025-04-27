from django import forms
from crispy_forms.helper import FormHelper
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'name', 'customer', 'reference', 'delivery_date', 'is_collection',
            'order_type', 'status', 'robes', 'cabs', 'panels', 'owner'
        ]
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control", "placeholder": " "}),
            'customer': forms.Select(attrs={"class": "form-select", "placeholder": " "}),
            'reference': forms.TextInput(attrs={"class": "form-control", "placeholder": " "}),
            'delivery_date': forms.DateInput(attrs={"type": "date", "class": "form-control", "placeholder": " "}),
            'is_collection': forms.CheckboxInput(attrs={"class": "form-check-input"}),
            'order_type': forms.Select(attrs={"class": "form-select", "placeholder": " "}),
            'status': forms.Select(attrs={"class": "form-select", "placeholder": " "}),
            'robes': forms.NumberInput(attrs={"class": "form-control", "placeholder": " "}),
            'cabs': forms.NumberInput(attrs={"class": "form-control", "placeholder": " "}),
            'panels': forms.NumberInput(attrs={"class": "form-control", "placeholder": " "}),
            'owner': forms.Select(attrs={"class": "form-select", "placeholder": " "}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
