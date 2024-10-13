from rest_framework import serializers
from .models import Collection, Movie

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'genres', 'uuid']

class CollectionSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True)

    class Meta:
        model = Collection
        fields = ['title', 'description', 'movies']
