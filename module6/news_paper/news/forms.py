from django import forms
from .models import *
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    content = forms.Textarea()

    class Meta:
        model = Post
        fields = ['author', 'title', 'content']

        def clean(self):
            cleaned_data = super().clean()
            content = cleaned_data.get('content')
            title = cleaned_data.get('title')
            if content == title:
                raise ValidationError(
                    "Текст статьи не должен повторять заголовок"
                )
            return cleaned_data


class UserForm(forms.ModelForm):
    content = forms.Textarea()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribers
        fields = [
            'category',
        ]
