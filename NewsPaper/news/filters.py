import django_filters
from django.forms.widgets import DateInput

from .models import Post


class PostFilter(django_filters.FilterSet):
    row_date = django_filters.DateFilter(label='After Date',
                                         lookup_expr='gt',
                                         field_name='time',
                                         widget=DateInput(attrs={'type': 'date'})
                                         )

    class Meta:
        model = Post
        fields = {
            'name': ['icontains'],
            'text': ['icontains'],
            'category': ['exact'],
        }


class PostCategoryFilter(django_filters.FilterSet):
    class Meta:
        model = Post
        fields = ['post_category']