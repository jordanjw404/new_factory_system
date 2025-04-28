from django import forms
from .models import ProductionStage
from orders.models import Order

class ProductionStageForm(forms.ModelForm):
    class Meta:
        model = ProductionStage
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['order'].queryset = Order.objects.select_related('customer')

        # Now customize each option
        choices = []
        for order in self.fields['order'].queryset:
            label = f"{order.reference} - {order.customer.name} ({order.delivery_date.strftime('%d %b %Y')})"
            choices.append((order.pk, label))

        self.fields['order'].choices = choices
