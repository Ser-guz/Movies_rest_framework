from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from .views import *
from . import api

# urlpatterns = format_suffix_patterns([
#     path('movie/', MovieViewSet.as_view({'get': 'list'})),
#     path('movie/<int:pk>/', MovieViewSet.as_view({'get': 'retrieve'})),
#     path('review/', ReviewCreateViewSet.as_view({'post': 'create'})),
#     path('rating/', AddStarRatingViewSet.as_view({'post': 'create'})),
#     path('actors/', api.ActorViewSet.as_view({'get': 'list'})),
#     path('actors/<int:pk>', api.ActorViewSet.as_view({'get': 'retrieve'})),
# ])

actor_list = api.ActorModelViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

actor_detail = api.ActorModelViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

actor_example = api.ActorModelViewSet.as_view({
    'get': 'example'
})

movie_list = api.MovieViewSet.as_view({
    'get': 'list',
})

movie_detail = api.MovieModelViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = format_suffix_patterns([
    path('actors/', actor_list, name='actor-list'),
    path('actors/<int:pk>', actor_detail, name='actor-detail'),
    path('actors/<int:pk>/example', actor_example, name='actor-example'),
    path('movie/', MovieViewSet.as_view({'get': 'list'})),
    path('movie/<int:pk>/', MovieViewSet.as_view({'get': 'retrieve'})),

])
#
# router = DefaultRouter()
# router.register(r'actor-read', api.ActorReadOnly, basename='actor')
# router.register(r'actor-modelset', api.ActorModelViewSet, basename='actor')
# urlpatterns = router.urls
