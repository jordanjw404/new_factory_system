from django import forms
from .models import Item, Location

class StockInForm(forms.Form):
    item = forms.ModelChoiceField(queryset=Item.objects.all())
    location = forms.ModelChoiceField(queryset=Location.objects.all())
    quantity = forms.DecimalField(max_digits=10, decimal_places=2)
    reason = forms.CharField(required=False)


class StockOutForm(forms.Form):
    item = forms.ModelChoiceField(queryset=Item.objects.all())
    location = forms.ModelChoiceField(queryset=Location.objects.all())
    quantity = forms.DecimalField(max_digits=10, decimal_places=2)
    reason = forms.CharField(required=False)


class TransferForm(forms.Form):
    item = forms.ModelChoiceField(queryset=Item.objects.all())
    from_location = forms.ModelChoiceField(queryset=Location.objects.all())
    to_location = forms.ModelChoiceField(queryset=Location.objects.all())
    quantity = forms.DecimalField(max_digits=10, decimal_places=2)
    reason = forms.CharField(required=False)
