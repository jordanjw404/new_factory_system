from decimal import Decimal
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, Div

class ProductActionForm(forms.Form):
    OP_CHOICES = [("IN","IN"), ("OUT","OUT"), ("MOVE","MOVE")]

    operation = forms.ChoiceField(
        choices=OP_CHOICES, initial="IN",
        widget=forms.Select(attrs={"class":"form-select", "id":"id_operation"})
    )
    qty = forms.DecimalField(
        min_value=Decimal("0.001"), max_digits=14, decimal_places=3,
        widget=forms.NumberInput(attrs={"class":"form-control"})
    )
    note = forms.CharField(
        max_length=120, required=False,
        widget=forms.TextInput(attrs={"class":"form-control"})
    )
    from_location = forms.CharField(
        max_length=64, required=False,
        widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"e.g. PICK-A01-B01-L01"})
    )
    to_location = forms.CharField(
        max_length=64, required=False,
        widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"e.g. PICK-A01-B01-L02"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        # Bootstrap 5 grid via crispy layout:
        self.helper.layout = Layout(
            Row(
                Column(Field("operation"), css_class="col-md-4"),
                Column(Field("qty"), css_class="col-md-4"),
                Column(Field("note"), css_class="col-md-4"),
                css_class="g-2"
            ),
            Div(Field("from_location"), css_id="fromFields", css_class="mt-2"),
            Div(Field("to_location"), css_id="toFields", css_class="mt-2"),
        )

    def clean(self):
        c = super().clean()
        op = c.get("operation"); fl = c.get("from_location"); tl = c.get("to_location")
        if op == "IN" and not tl:
            raise forms.ValidationError("Destination location is required for IN.")
        if op == "OUT" and not fl:
            raise forms.ValidationError("Source location is required for OUT.")
        if op == "MOVE":
            if not fl or not tl:
                raise forms.ValidationError("Both source and destination are required for MOVE.")
            if fl == tl:
                raise forms.ValidationError("Source and destination must differ for MOVE.")
        return c
