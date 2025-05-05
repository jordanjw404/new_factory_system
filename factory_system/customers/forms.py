from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, ButtonHolder
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            "name", "contact_name", "email", "phone", "mobile",
            "address_1", "address_2", "city", "postcode", "notes", "is_active"
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": " "}),
            "contact_name": forms.TextInput(attrs={"class": "form-control", "placeholder": " "}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": " "}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": " "}),
            "mobile": forms.TextInput(attrs={"class": "form-control", "placeholder": " "}),
            "address_1": forms.TextInput(attrs={"class": "form-control", "placeholder": " "}),
            "address_2": forms.TextInput(attrs={"class": "form-control", "placeholder": " "}),
            "city": forms.TextInput(attrs={"class": "form-control", "placeholder": " "}),
            "postcode": forms.TextInput(attrs={"class": "form-control", "placeholder": " "}),
            "notes": forms.Textarea(attrs={"class": "form-control", "placeholder": " ", "rows": 3}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column("name", css_class="col-md-6"),
                Column("contact_name", css_class="col-md-6"),
            ),
            Row(
                Column("email", css_class="col-md-6"),
                Column("phone", css_class="col-md-6"),
            ),
            Row(
                Column("mobile", css_class="col-md-6"),
                Column("address_1", css_class="col-md-6"),
            ),
            Row(
                Column("address_2", css_class="col-md-6"),
                Column("city", css_class="col-md-6"),
            ),
            Row(
                Column("postcode", css_class="col-md-4"),
                Column("notes", css_class="col-md-4"),
                Column("is_active", css_class="col-md-4"),
            ),
            ButtonHolder(
                Submit("submit", "Save Customer", css_class="btn btn-primary w-100 mt-3")
            )
        )

from django import forms

class CustomerImportForm(forms.Form):
    csv_file = forms.FileField(label='Upload CSV file')
