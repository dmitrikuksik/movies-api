from django.conf import settings
from rest_framework import serializers
from .models import Movie
import requests

class MovieTitleSerializer(serializers.Serializer):
    title = serializers.CharField()

    movie_data = {}
    is_exist = False

    def validate_title(self, title):
        self.movie_data = settings.OMDB_CLIENT.get(title=title,
                                                  fullplot=True,
                                                  tomatoes=False)
        if not self.movie_data:
            raise serializers.ValidationError("Movie with such title doesn't exist.")
        
        exist = Movie.objects.filter(data__title=self.movie_data['title']).first()
        if exist:
            self.is_exist = True
            return exist.data['title']
    
        return self.movie_data['title']

    def save(self):
        if not self.is_exist:
            movie = Movie.objects.create(data=self.movie_data)
            movie.save()
        else:
            movie = Movie.objects.filter(data__title=self.validated_data['title']).first()
        return movie

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

                                                




        