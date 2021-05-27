from home.models import *
from django import forms
from mptt.forms import TreeNodeChoiceField
from django.utils.safestring import mark_safe

class ItemForm(forms.ModelForm):
    image = forms.ImageField(label='画像', required=False)
    category = TreeNodeChoiceField(label='カテゴリー', queryset=Category.objects.all(), level_indicator="|")
    class Meta:
        model = MenuItem
        fields = ['name', 'category','price', 'image', 'description', 'quantity']

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "お名前"
        self.fields['price'].label = "単価"
        self.fields['description'].label = "詳細"
        self.fields['quantity'].label = "在庫数"