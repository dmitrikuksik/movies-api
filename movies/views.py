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


    def get(self, request, format='JSON'):
        movies = Movie.objects.all()        
        if not movies:
            return Response(
                status=status.HTTP_200_OK,
                data={"data":"There are no movies in database."})        
        serializer = MovieSerializer(
                        movies,
                        many=True
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

    def get(self, request, format='JSON'):
        comments = Comment.objects.all()
        if not comments:
            return Response(
                status=status.HTTP_200_OK,
                data={"data":"There are no comments in database."}
                )
        serializer = CommentSerializer(
                        comments,
                        many=True
                        )
        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )
        
    
        
        