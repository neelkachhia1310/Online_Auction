import django_filters
from .models import Post
from users.models import Profile
from django.contrib.auth.models import User


class PostFilter(django_filters.FilterSet):

    CHOICES = {
        ('ascending','Ascending'),
        ('decending','Decending')
    }
    ordering = django_filters.ChoiceFilter(label='Ordering', choices=CHOICES, method='filter_by_order')

    class Meta:
        model=Post
        fields ={
            'title' : ['icontains'],
            'author__username' : ['icontains'],
            'base_price' : ['icontains'],
        }

    def filter_by_order(self, queryset, name, value):
        expression = 'title' if value == 'ascending' else '-title' 
        return queryset.order_by(expression)