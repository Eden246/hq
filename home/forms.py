from .models import *
from django import forms

class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','password','email']
        widgets = {
        'password': forms.PasswordInput(),
        'email': forms.EmailInput(),
        }

class ClientForm(forms.ModelForm):
    class Meta:
        model=Client
        fields=['facility','phone']

class PostForm(forms.ModelForm):
    body = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows':'5',
            'placeholder':'内容を入力してください'
            }))

    image = forms.ImageField(label='画像',required=False,widget=forms.ClearableFileInput(attrs={'multiple':True}))

    class Meta:
        model = Post
        fields=['body']

class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows':'3',
            }))
    class Meta:
        model = Comment
        fields=['comment']

class ThreadForm(forms.Form):
    username = forms.fields.ChoiceField(label='',
        choices = (
            ('鈴木一郎', '鈴木一郎'),
        ),
        required=True,
        widget=forms.widgets.Select(attrs={'size':'5','style': 'width: 100%'})
    )
class MessageForm(forms.Form):
    message = forms.CharField(label='',max_length=1000,
    widget=forms.TextInput(attrs={'style': 'width: 100%'})
    )