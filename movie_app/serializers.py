from rest_framework import serializers
from .models import Movie, Review, Director


class DirectorSerializer(serializers.ModelSerializer):
    movie_count = serializers.SerializerMethodField()

    class Meta:
        model = Director
        fields = ('name', 'movie_count')

    def get_movie_count(self, director):
        return director.movies.count()


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('text', 'movie', 'stars')


class MovieSerializer(serializers.ModelSerializer):
    director = DirectorSerializer()
    reviews = ReviewSerializer(many=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ('title', 'description', 'duration', 'director', 'reviews', 'average_rating')

    def get_average_rating(self, movie):
        reviews = movie.reviews.all()
        if reviews:
            sum_reviews = sum([review.stars for review in reviews]) #6
            average = sum_reviews / len(reviews) # 6/2 = 3
            return average
        return None
        