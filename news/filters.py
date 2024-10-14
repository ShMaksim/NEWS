from django_filters import FilterSet, CharFilter, DateFilter
from .models import Post
from django.forms.widgets import DateInput

class PostFilter(FilterSet):
    title = CharFilter(field_name='title',lookup_expr='icontains', label='Название')
    author = CharFilter(field_name='author__user__username', lookup_expr='icontains', label='Автор')
    created_at = DateFilter(
        field_name='created_at',
        lookup_expr='gte',
        label='Позже даты',
        widget=DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Post
        fields = ['title', 'author', 'created_at']
