from .serializers import *
from .models import Movie, Comment
from .filters import MovieFilter

from rest_framework.response import Response
from rest_framework import status, viewsets, mixins
from django_filters.rest_framework import DjangoFilterBackend


# class Movies(APIView):

#     def post(self, request, format='JSON'):
#         serializer = MovieTitleSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             movie = serializer.save()
#             serializer = MovieSerializer(movie)
#             return Response(
#                 status=status.HTTP_200_OK,
#                 data=serializer.data
#             )

#     def get(self, request, format='JSON', **kwargs):
#         movie_id = kwargs.get('movie_id', None)
#         if movie_id:
#             try:
#                 movie = Movie.objects.get(movie_id=movie_id)
#                 serializer = MovieSerializer(movie)
#             except:
#                 return Response(
#                     status=status.HTTP_404_NOT_FOUND,
#                 )
#         else:
#             if not request.query_params:
#                 movies = Movie.objects.all()
#             else:
#                 order_by = request.query_params.get('order_by', None)
#                 year = request.query_params.get('year', None)
#                 if order_by and year:
#                     movies = Movie.objects.filter(
#                         data__year=year
#                     ).order_by(order_by)
#                 elif order_by:
#                     movies = Movie.objects.all().order_by(order_by)
#                 elif year:
#                     movies = Movie.objects.filter(data__year=year)
#                 else:
#                     return Response(
#                         status=status.HTTP_400_BAD_REQUEST,
#                         data={
#                             "error": "Something went wrong."
#                         })
#             try:
#                 serializer = MovieSerializer(movies, many=True)
#                 return Response(
#                         status=status.HTTP_200_OK,
#                         data=serializer.data
#                 )
#             except:
#                 return Response(
#                     status=status.HTTP_400_BAD_REQUEST,
#                     data={
#                         "error": "Something went wrong."
#                     })


class MovieViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):

    queryset = Movie.objects.all().order_by('movie_id')
    filter_backends = (DjangoFilterBackend,)
    filter_class = MovieFilter

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


class CommentViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     viewsets.GenericViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('movie_id',)
