import django.forms
from django_filters import FilterSet, DateFilter
from .models import *


class PostFilter(FilterSet):
    publishing_date = DateFilter(
        lookup_expr='gt', widget=django.forms.DateInput(attrs={'type': 'date'}
                                                        )
    )

    class Meta:
        model = Post
        fields = {
            'content': ['icontains'],
            'title': ['icontains'],
            'type': ['exact'],
        }
