# production/forms.py
from django import forms
from .models import ProductionStage

class ProductionStageForm(forms.ModelForm):
    class Meta:
        model = ProductionStage
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Automatically set all DateFields to have a date picker
        for field_name, field in self.fields.items():
            if isinstance(field, forms.DateField):
                field.widget = forms.DateInput(
                    attrs={'type': 'date', 'class': 'form-control form-control-sm'}
                )
