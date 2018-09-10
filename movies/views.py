from django.shortcuts import render

from .serializers import MovieTitleSerializer, MovieSerializer

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
                data=serializer.data)


