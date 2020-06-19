from rest_framework import viewsets
from django.db import models
from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend

from .servise import get_client_ip, MovieFilter, PaginationMovie
from .models import Movie
from .serializers import *


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод списка фильмов"""
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter
    pagination_class = PaginationMovie

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            midle_star=(models.Avg("ratings__star"))
        )
        return movies

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        if self.action == 'retrieve':
            return MovieDetailSerializer


class ReviewCreateViewSet(viewsets.ModelViewSet):
    """Добавление отзыва к фильму"""
    serializer_class = ReviewCreateSerializer


class AddStarRatingViewSet(viewsets.ModelViewSet):
    """Добавление рейтинга фильму"""
    serializer_class = RatingCreateSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request)) 


class ActorViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод списка актёров и режисёров"""
    queryset = Actor.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        if self.action == 'retrieve':
            return MovieDetailSerializer


