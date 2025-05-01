from django import forms
from .models import Item, Location,IncomingOrder, IncomingOrderItem
from django.forms import inlineformset_factory

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



class IncomingOrderForm(forms.ModelForm):
    class Meta:
        model = IncomingOrder
        fields = ['supplier', 'order_ref', 'expected_date']

IncomingOrderItemFormSet = inlineformset_factory(
    IncomingOrder, IncomingOrderItem,
    fields=('item', 'quantity_expected', 'unit_cost', 'location'),
    extra=5, can_delete=False
)


