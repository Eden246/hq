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
            'placeholder':'担当者が直ちに、ご返信させていただきます！画像アップが必要な方は「ファイルの選択」ボタンをクリックしてください。（不正書き込みは削除されますので、ご了承ください）'
            }))

    image = forms.ImageField(label='画像',required=False)

    class Meta:
        model = Post
        fields=['body','image']

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
            ('鈴木', '鈴木'),
            ('田中', '田中'),
            ('佐藤', '佐藤'),
            ('スタッフ', '営業所'),
        ),
        required=True,
        widget=forms.widgets.Select(attrs={'size':'5','style': 'width: 100%'})
    )
class MessageForm(forms.Form):
    message = forms.CharField(label='',max_length=1000,
    widget=forms.TextInput(attrs={'style': 'width: 100%'})
    )