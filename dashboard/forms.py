from home.models import *
from django import forms

class ItemForm(forms.ModelForm):
    image = forms.ImageField(label='画像',required=False)

    class Meta:
        model = MenuItem
        fields = ['name', 'category', 'quantity', 'price', 'image', 'description']
        