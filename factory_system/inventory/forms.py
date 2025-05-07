from django import forms
from django.forms import inlineformset_factory
from .models import Item, Location, IncomingOrder, IncomingOrderItem, BoardStock, ItemStock


# Form for adding stock to a specific location
class StockInForm(forms.Form):
    item = forms.ModelChoiceField(queryset=Item.objects.all())
    location = forms.ModelChoiceField(queryset=Location.objects.all())
    quantity = forms.DecimalField(max_digits=10, decimal_places=2)
    reason = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        item = cleaned_data.get("item")
        location = cleaned_data.get("location")
        quantity = cleaned_data.get("quantity")

        # Ensure quantity is positive
        if quantity <= 0:
            raise forms.ValidationError("Quantity must be greater than zero.")

        return cleaned_data


# Form for removing stock from a specific location
class StockOutForm(forms.Form):
    item = forms.ModelChoiceField(queryset=Item.objects.all())
    location = forms.ModelChoiceField(queryset=Location.objects.all())
    quantity = forms.DecimalField(max_digits=10, decimal_places=2)
    reason = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        item = cleaned_data.get("item")
        location = cleaned_data.get("location")
        quantity = cleaned_data.get("quantity")

        # Check available stock
        stock = ItemStock.objects.filter(item=item, location=location).first()
        if not stock or stock.quantity < quantity:
            raise forms.ValidationError(f"Not enough stock for {item.name} at {location.name}.")

        return cleaned_data


# Form for transferring stock between locations
class TransferForm(forms.Form):
    item = forms.ModelChoiceField(queryset=Item.objects.all())
    from_location = forms.ModelChoiceField(queryset=Location.objects.all())
    to_location = forms.ModelChoiceField(queryset=Location.objects.all())
    quantity = forms.DecimalField(max_digits=10, decimal_places=2)
    reason = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        item = cleaned_data.get("item")
        from_location = cleaned_data.get("from_location")
        to_location = cleaned_data.get("to_location")
        quantity = cleaned_data.get("quantity")

        # Prevent transferring to the same location
        if from_location == to_location:
            raise forms.ValidationError("Cannot transfer to the same location.")

        # Check available stock at source location
        stock = ItemStock.objects.filter(item=item, location=from_location).first()
        if not stock or stock.quantity < quantity:
            raise forms.ValidationError(f"Not enough stock for {item.name} at {from_location.name}.")

        return cleaned_data


# Form for creating incoming orders
class IncomingOrderForm(forms.ModelForm):
    class Meta:
        model = IncomingOrder
        fields = ['supplier', 'order_ref', 'expected_date']


# Inline formset for adding items to an incoming order
IncomingOrderItemFormSet = inlineformset_factory(
    IncomingOrder, IncomingOrderItem,
    fields=('item', 'quantity_expected', 'unit_cost', 'location'),
    extra=5,
    can_delete=False
)


# Form for adding or editing items in the inventory
class AddItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'code', 'name', 'type', 'description',
            'width', 'length', 'height', 'thickness',
            'color', 'unit', 'reorder_level', 'standard_cost', 'supplier'
        ]
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'width': forms.NumberInput(attrs={'class': 'form-control'}),
            'length': forms.NumberInput(attrs={'class': 'form-control'}),
            'height': forms.NumberInput(attrs={'class': 'form-control'}),
            'thickness': forms.NumberInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'unit': forms.TextInput(attrs={'class': 'form-control'}),
            'reorder_level': forms.NumberInput(attrs={'class': 'form-control'}),
            'standard_cost': forms.NumberInput(attrs={'class': 'form-control'}),
        }


# Form for creating and editing board stock (offcuts)
class BoardStockForm(forms.ModelForm):
    class Meta:
        model = BoardStock
        fields = ['parent_board', 'location', 'is_offcut', 'notes', 'dimensions']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

    def clean(self):
        cleaned_data = super().clean()
        parent_board = cleaned_data.get("parent_board")
        dimensions = cleaned_data.get("dimensions", {})

        # Validate that length and width are provided
        length = dimensions.get("length")
        width = dimensions.get("width")
        
        if not length or not width:
            raise forms.ValidationError("Both length and width are required for board stock.")

        # Validate that the piece is not larger than the full board
        piece_area = length * width
        full_area = parent_board.width * parent_board.length if parent_board.width and parent_board.length else 0
        
        if full_area == 0:
            raise forms.ValidationError("Parent board must have valid width and length.")
        
        if piece_area > full_area:
            raise forms.ValidationError("Piece cannot be larger than the parent board.")

        return cleaned_data
