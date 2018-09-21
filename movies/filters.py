import django_filters
from .models import Movie


class MovieFilter(django_filters.FilterSet):
    year = django_filters.CharFilter(
        field_name='data__year'
    )
    country = django_filters.CharFilter(
        field_name='data__country'
    )
    imdb_rating = django_filters.CharFilter(
        field_name='data__imdb_rating'
    )

    class Meta:
        model = Movie
        fields = [
            'year',
            'country',
            'imdb_rating'
        ]
