from django.shortcuts import render
from rest_framework import generics
from .models import Movie, Review, Director
from .serializers import MovieSerializer, ReviewSerializer, DirectorSerializer, MovieValidirySerializer, ReviewValiditySerializer
from rest_framework.response import Response
from rest_framework import status


class DirectorListAPIView(generics.ListCreateAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer


class DirectorDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    lookup_field = 'id'


class MovieListAPIView(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def post(self, request, *args, **kwargs):
        validator = MovieValidirySerializer(data=request.data)
        if not validator.is_valid():
            return Response(validator.errors, status=status.HTTP_400_BAD_REQUEST)
        title = validator.validated_data['title']
        description = validator.validated_data['description']
        duration = validator.validated_data['duration']
        director_id = validator.validated_data['director']
        movie = Movie.objects.create(title=title, description=description, duration=duration, director_id=director_id)
        movie.save()
        return Response(MovieSerializer(movie).data, status=status.HTTP_201_CREATED)
            

class MovieDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        movie_detail = self.get_object()
        validator = MovieValidirySerializer(data=request.data)
        if not validator.is_valid():
            return Response(validator.errors, status=status.HTTP_400_BAD_REQUEST)
        movie_detail.title = validator.validated_data['title']
        movie_detail.description = validator.validated_data['description']
        movie_detail.duration = validator.validated_data['duration']
        movie_detail.director_id = validator.validated_data['director']
        movie_detail.save()
        return Response(MovieSerializer(movie_detail).data, status=status.HTTP_200_OK)


class ReviewListAPIView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def post(self, request, *args, **kwargs):
        validator = ReviewValiditySerializer(data=request.data)
        if not validator.is_valid():
            return Response(validator.errors, status=status.HTTP_400_BAD_REQUEST)
        text = validator.validated_data['text']
        movie_id = validator.validated_data['movie']
        stars = validator.validated_data['stars']
        review = Review.objects.create(text=text, movie_id=movie_id, stars=stars)
        review.save()
        return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)


class ReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        review_detail = self.get_object()
        validator = ReviewValiditySerializer(data=request.data)
        if not validator.is_valid():
            return Response(validator.errors, status=status.HTTP_400_BAD_REQUEST)
        review_detail.text = validator.validated_data['text']
        review_detail.movie_id = validator.validated_data['movie']
        review_detail.stars = validator.validated_data['stars']
        review_detail.save()
        return Response(ReviewSerializer(review_detail).data, status=status.HTTP_200_OK)
