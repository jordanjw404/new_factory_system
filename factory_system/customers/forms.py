from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field
from .models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            "name", "contact_name", "email", "phone", "mobile",
            "address_1", "address_2", "city", "postcode", "notes", "is_active"
        ]
        widgets = {
            'address_1': forms.TextInput(attrs={'placeholder': 'Address Line 1'}),
            'address_2': forms.TextInput(attrs={'placeholder': 'Address Line 2'}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "form-horizontal" 
        self.helper.label_class = "col-sm-4 col-form-label"
        self.helper.field_class = "col-sm-8"

        self.helper.layout = Layout(
            Row(
                Column(Field("name"), css_class="mb-3"),
                Column(Field("contact_name"), css_class="mb-3"),
            ),
            Row(
                Column(Field("email"), css_class="mb-3"),
                Column(Field("phone"), css_class="mb-3"),
                Column(Field("mobile"), css_class="mb-3"),
            ),
            Row(
                Column(Field("address_1"), css_class="mb-3"),
                Column(Field("address_2"), css_class="mb-3"),
            ),
            Row(
                Column(Field("city"), css_class="mb-3"),
                Column(Field("postcode"), css_class="mb-3"),
            ),
            Field("notes"),
            Field("is_active"),
            Submit("submit", "Save Customer", css_class="btn btn-primary w-100 mt-3")
        )
