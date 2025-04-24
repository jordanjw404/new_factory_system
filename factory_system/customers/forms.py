from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            "name", "contact_name", "email", "phone", "mobile",
            "address_1", "address_2", "city", "postcode", "notes", "is_active"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column("name", css_class="col-sm-6"),
                Column("contact_name", css_class="col-sm-6"),
            ),
            Row(
                Column("email", css_class="col-sm-6"),
                Column("phone", css_class="col-sm-3"),
                Column("mobile", css_class="col-sm-3"),
            ),
            Row(
                Column("address_1", css_class="col-sm-6"),
                Column("address_2", css_class="col-sm-6"),
            ),
            Row(
                Column("city", css_class="col-sm-6"),
                Column("postcode", css_class="col-sm-6"),
            ),
            "notes",
            "is_active",
            Submit("submit", "Save Customer", css_class="btn btn-primary w-100 mt-3")
        )
