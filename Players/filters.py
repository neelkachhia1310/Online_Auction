import django_filters
from .models import player


class PlayerFilter(django_filters.FilterSet):

    CHOICES = {
        ('ascending','Ascending'),
        ('decending','Decending')
    }
    ordering = django_filters.ChoiceFilter(label='Ordering', choices=CHOICES, method='filter_by_order')

    class Meta:
        model=player
        fields ={
            'player_name' : ['icontains'],
            'sell_teamName' : ['icontains'],
        }

    def filter_by_order(self, queryset, name, value):
        expression = 'player_name' if value == 'ascending' else '-player_name' 
        return queryset.order_by(expression)