from django import forms
from .models import Variant

class VariantForm(forms.ModelForm):
    class Meta:
        model = Variant
        fields = ['buying_price','commission_percentage']  # Include the buying_price field in the form
