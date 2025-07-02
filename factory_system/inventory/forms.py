from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row, Submit
from django import forms

from .models import Supplier


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = "__all__"
        widgets = {
            "address": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column(FloatingField("name"), css_class="mb-3"),
                Column(FloatingField("contact_name"), css_class="mb-3"),
            ),
            Row(
                Column(FloatingField("phone"), css_class="mb-3"),
                Column(FloatingField("email"), css_class="mb-3"),
            ),
            FloatingField("address"),
            Submit("submit", "Save Supplier", css_class="btn btn-success w-100 mt-4"),
        )
