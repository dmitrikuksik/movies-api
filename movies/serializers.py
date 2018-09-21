from django.conf import settings
from rest_framework import serializers
from .models import Movie, Comment


class MovieTitleSerializer(serializers.Serializer):
    title = serializers.CharField()

    movie_data = {}

    def validate_title(self, title):
        self.movie_data = settings.OMDB_CLIENT.get(
            title=title,
            fullplot=True,
            tomatoes=False
        )
        if not self.movie_data:
            raise serializers.ValidationError(
                "Movie with such title doesn't exist."
            )

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
