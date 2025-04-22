from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class meta:
        model = Customer
        fields = ["name","Contact Name", "email", "phone_number", "Mobile Number", "address_1", "address_2", "city", "postcode", "notes"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Enter customer name"}),
            "Contact Name": forms.TextInput(attrs={"placeholder": "Enter contact name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Enter email address"}),
            "phone_number": forms.TextInput(attrs={"placeholder": "Enter phone number"}),
            "Mobile Number": forms.TextInput(attrs={"placeholder": "Enter mobile number"}),
            "address_1": forms.Textarea(attrs={"placeholder": "Enter address 1"}),
            "address_2": forms.Textarea(attrs={"placeholder": "Enter address 2"}),
            "city": forms.TextInput(attrs={"placeholder": "Enter city"}),
            "postcode": forms.TextInput(attrs={"placeholder": "Enter postcode"}),
            "notes": forms.Textarea(attrs={"placeholder": "Enter notes"}),
        }

