from django.db import models
from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend

from .servise import get_client_ip, MovieFilter
from .models import Movie
from .serializers import *


class MovieListView(generics.ListAPIView):
    """Вывод списка фильмов"""
    serializer_class = MovieListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            midle_star=(models.Avg("ratings__star"))
        )
        return movies


class MovieDetailView(generics.RetrieveAPIView):
    """Вывод полного фильма"""
    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer


class ReviewCreateView(generics.CreateAPIView):
    """Добавление отзыва к фильму"""
    serializer_class = ReviewCreateSerializer


class AddStarRatingView(generics.CreateAPIView):
    """Добавление рейтинга фильму"""
    serializer_class = RatingCreateSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request)) 


class ActorListView(generics.ListAPIView):
    """Вывод списка актёров и режисёров"""
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorDetailView(generics.RetrieveAPIView):
    """Вывод полной информации об актёрах и режисёрах"""
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer
