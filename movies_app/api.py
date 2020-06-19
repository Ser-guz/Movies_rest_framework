from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import models

from movies_app.servise import get_client_ip
from .models import Actor, Movie
from .serializers import (
    ActorListSerializer,
    ActorDetailSerializer,
    MovieListSerializer,
    MovieDetailSerializer
)


class MovieViewSet(viewsets.ViewSet):
    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            midle_star=(models.Avg("ratings__star"))
        )
        return movies

    def list(self, request):
        queryset = Movie.objects.filter(draft=False)
        serializer = MovieListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Movie.objects.filter(draft=False)
        movie = get_object_or_404(queryset, pk=pk)
        serializer = MovieDetailSerializer(movie)
        return Response(serializer.data)


class MovieModelViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieListSerializer

    @action(detail=True)
    def example(self, request, *args, **kwargs):
        movie = self.get_object()
        serializer = MovieDetailSerializer(movie)
        return Response(serializer.data)


class ActorViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Actor.objects.all()
        serializer = ActorListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Actor.objects.all()
        actor = get_object_or_404(queryset, pk=pk)
        serializer = ActorDetailSerializer(actor)
        return Response(serializer.data)


class ActorReadOnly(viewsets.ReadOnlyModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorModelViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer

    @action(detail=True)
    def example(self, request, *args, **kwargs):
        actor = self.get_object()
        serializer = ActorDetailSerializer(actor)
        return Response(serializer.data)