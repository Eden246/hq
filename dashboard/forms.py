from django.forms import fields
from home.models import *
from django import forms
from mptt.forms import TreeNodeChoiceField
from .models import *
from django.urls import reverse

class ItemForm(forms.ModelForm):
    category = TreeNodeChoiceField(label='カテゴリー', queryset=Category.objects.all(), level_indicator="|")
    class Meta:
        model = MenuItem
        fields = ['name', 'category','price', 'image', 'description', 'quantity', 'video_url']

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "お名前"
        self.fields['price'].label = "単価"
        self.fields['description'].label = "詳細"
        self.fields['quantity'].label = "在庫数"
        self.fields['image'].label = "品目画像"
        self.fields['video_url'].label = "商品動画URL"

class TextForm(forms.ModelForm):
    class Meta:
        model = Text
        fields = ('__all__')
    
    def __init__(self, *args, **kwargs):
        super(TextForm, self).__init__(*args, **kwargs)
        self.fields['first'].label = "1番目"
        self.fields['second'].label = "2番目"
        self.fields['third'].label = "3番目"

class ImageForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = ['image',]
    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.fields['image'].label = "《契約書》"

class TrackerImageForm(forms.ModelForm):
    class Meta:
        model = Tracker
        fields = ['contract_image']
    def __init__(self, *args, **kwargs):
        super(TrackerImageForm, self).__init__(*args, **kwargs)
        self.fields['contract_image'].label = "受渡確認書"