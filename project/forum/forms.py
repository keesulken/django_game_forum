from django import forms
from django.core.exceptions import ValidationError

from .models import Adv, AdvReply


class AdvForm(forms.ModelForm):
    content = forms.Textarea()

    class Meta:
        model = Adv
        fields = ['author', 'guild', 'title', 'content']

        def clean(self):
            cleaned_data = super().clean()
            content = cleaned_data.get('content')
            title = cleaned_data.get('title')
            if content == title:
                raise ValidationError(
                    "Текст объявления не должен повторять заголовок"
                )
            return cleaned_data


class AdvReplyForm(forms.ModelForm):
    class Meta:
        model = AdvReply
        fields = ['content', 'adv', ]


class AdvReplyStatusForm(forms.ModelForm):
    class Meta:
        model = AdvReply
        fields = ['status', ]
