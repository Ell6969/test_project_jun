from django import forms
from .models import Products


class ProductsForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'price', 'description', 'image']


class ProductFilterForm(forms.Form):
    min_price = forms.DecimalField(label='Минимальная цена', required=False)
    max_price = forms.DecimalField(label='Максимальная цена', required=False)
    start_date = forms.DateField(label='Дата начала', required=False)
    end_date = forms.DateField(label='Дата окончания', required=False)
