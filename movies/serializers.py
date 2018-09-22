from django.conf import settings
from rest_framework import serializers
from .models import Movie, Comment
from omdb.omdb import OMDBClient


class MovieTitleSerializer(serializers.Serializer):
    title = serializers.CharField()

    movie_data = {}

    def validate_title(self, title):
        self.movie_data = OMDBClient().get_data_by_title(title)
        exist = Movie.objects.filter(
            data__title=self.movie_data['title']
        ).first()

        if exist:
            self.instance = exist
            return exist.data['title']

        return self.movie_data['title']

    def update(self, instance, validated_data):
        return instance

    def create(self, validated_data):
        movie = Movie.objects.create(data=self.movie_data)
        movie.save()
        return movie


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
