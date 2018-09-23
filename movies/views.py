from .serializers import *
from .models import Movie, Comment
from .filters import MovieFilter

from rest_framework.response import Response
from rest_framework import status, viewsets, mixins
from django_filters.rest_framework import DjangoFilterBackend


class MovieViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):

    queryset = Movie.objects.all().order_by('movie_id')
    filter_class = MovieFilter
    ordering_fields = (
        'movie_id',
        'data__year',
        'data__imdbrating',
        'data__title',
    )

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MovieTitleSerializer
        return MovieSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        movie = serializer.save()
        response_serializer = MovieSerializer(movie)

        return Response(
            status=status.HTTP_200_OK,
            data=response_serializer.data
        )

    def list(self, request, *args, **kwargs):
        if (
            request.query_params and
            not request.query_params.get('year') and
            not request.query_params.get('country') and
            not request.query_params.get('imdb_rating') and
            not request.query_params.get('ordering')
        ):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CommentViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     viewsets.GenericViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_fields = ('movie_id',)
