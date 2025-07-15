from django import forms

# from config.channel.models import Channel
from .models import Group


class CreateGroupForm(forms.ModelForm):
    name = forms.CharField(
        max_length=150,
        required=True,
        label='Название группы',
        widget=forms.TextInput(
            attrs={
                'id': 'groupName',
                'class': 'form-control',
                'autofocus': True,
                'name': 'name',
            }
        )
    )
    description = forms.CharField(
        required=False,
        label='Описание',
        widget=forms.Textarea(
            attrs={
                'id': 'groupDescription',
                'class': 'form-control',
                'rows': 3,
                'name': 'description',
            }
        )
    )
    image_url = forms.CharField(
        required=False,
        label='Изображение (URL)',
        widget=forms.URLInput(
            attrs={
                'id': 'groupImage',
                'placeholder': 'https://example.com/image.jpg',
                'class': 'form-control',
                'name': 'image_url',
            }
        )
    )
    
    class Meta:
        model = Group
        fields = ('name', 'description', 'image_url',)
        
        
class UpdateGroupForm(forms.ModelForm):
    name = forms.CharField(
        max_length=150,
        required=True,
        label='Название группы',
        widget=forms.TextInput(
            attrs={
                'id': 'editGroupName',
                'class': 'form-control',
                'autofocus': True,
                'name': 'name',
            }
        )
    )
    description = forms.CharField(
        required=False,
        label='Описание',
        widget=forms.Textarea(
            attrs={
                'id': 'editGroupDescription',
                'class': 'form-control',
                'rows': 3,
                'name': 'description',
            }
        )
    )
    image_url = forms.CharField(
        required=False,
        label='Изображение (URL)',
        widget=forms.URLInput(
            attrs={
                'id': 'editGroupImage',
                'placeholder': 'https://example.com/image.jpg',
                'class': 'form-control',
                'name': 'image_url',
            }
        )
    )
    
    class Meta:
        model = Group
        fields = ('name', 'description', 'image_url',)