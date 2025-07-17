from django import forms


class ChannelParseForm(forms.Form):
    channel_identifier = forms.CharField(
        label='ID канала username или ссылка',
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите ID канала username или ссылку на канал',
            'class': 'form-control'
        })
    )
    limit = forms.IntegerField(
        label='Количество постов',
        min_value=1,
        max_value=20,
        initial=10,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
