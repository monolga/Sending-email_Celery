from django_filters import FilterSet,DateTimeFilter
from django.forms import DateTimeInput
from .models import*

class PostFilter(FilterSet):
    dateCreation = DateTimeFilter(
        field_name='dateCreation',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%',
            attrs={'type': 'datetime-local'},
        ),
    )
    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'categoryType':['contains'],
       }
