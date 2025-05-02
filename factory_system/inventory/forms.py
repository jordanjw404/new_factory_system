from django import forms
from .models import Item, Location, IncomingOrder, IncomingOrderItem
from django.forms import inlineformset_factory
from django import forms
from .models import BoardStock, Item, Location

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

class AddItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'code', 'name', 'type', 'description',
            'width', 'length', 'height', 'depth',
            'thickness', 'color', 'unit', 'reorder_level'
        ]
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'width': forms.NumberInput(attrs={'class': 'form-control'}),
            'length': forms.NumberInput(attrs={'class': 'form-control'}),
            'height': forms.NumberInput(attrs={'class': 'form-control'}),
            'depth': forms.NumberInput(attrs={'class': 'form-control'}),
            'thickness': forms.NumberInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'unit': forms.TextInput(attrs={'class': 'form-control'}),
            'reorder_level': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class BoardStockForm(forms.ModelForm):
    class Meta:
        model = BoardStock
        fields = ['parent_board', 'length', 'width', 'thickness', 'location', 'is_offcut', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2}),
        }
