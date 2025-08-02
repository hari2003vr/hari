from .models import *
from django import forms

class update_form(forms.ModelForm):
    class Meta:
        model=product_table
        fields='__all__'