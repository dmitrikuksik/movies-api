from django.shortcuts import render

from .serializers import MovieTitleSerializer, MovieSerializer, CommentSerializer
from .models import Movie, Comment

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class Movies(APIView):

    def post(self, request, format='JSON'):
        serializer = MovieTitleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            movie = serializer.save()
            serializer = MovieSerializer(movie)
            return Response(
                status=status.HTTP_200_OK,
                data=serializer.data
                )

    def get(self, request, format='JSON', **kwargs):
        movie_id = kwargs.get('movie_id',None)
        if movie_id:
            try:
                movie = Movie.objects.get(movie_id=movie_id)
                serializer = MovieSerializer(movie)
            except:
                return Response(
                    status=status.HTTP_200_OK,
                    data={"data":"There are no movie for this request."})
        else:
            if not request.query_params:
                movies = Movie.objects.all()
                serializer = MovieSerializer(movies,many=True)
            else:
                order_by = request.query_params.get('order_by',None)
                year = request.query_params.get('year',None)
                if order_by and year:
                    movies = Movie.objects.filter(data__year=year).order_by(order_by)
                    serializer = MovieSerializer(movies,many=True)
                elif order_by:
                    movies = Movie.objects.all().order_by(order_by)
                    serializer = MovieSerializer(movies,many=True)
                elif year:
                    movies = Movie.objects.filter(data__year=year)
                    serializer = MovieSerializer(movies,many=True)
                else:
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data={"error":"Something went wrong."}
                        )
                try:
                    if not movies:
                        return Response(
                            status=status.HTTP_200_OK,
                            data={"data":"There are no movie for this request."})
                except:
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data={"error":"Something went wrong."}
                        )

        return Response(
                status=status.HTTP_200_OK,
                data=serializer.data
                )

class Comments(APIView):
    
    def post(self, request, format='JSON'):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            comment = serializer.save()
            serializer = CommentSerializer(comment)
            return Response(
                status=status.HTTP_200_OK,
                data={"text":serializer.data['text']}
                )

    def get(self, request, format='JSON', **kwargs):
        movie_id = kwargs.get('movie_id', None)
        if movie_id:
            comments = Comment.objects.filter(movie_id=movie_id)
        else:
            comments = Comment.objects.all()
        if not comments:
            return Response(
                status=status.HTTP_200_OK,
                data={"data":"There are no comments for this request."}
                )
        serializer = CommentSerializer(
                        comments,
                        many=True
                        )
        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )
        
    
        
        