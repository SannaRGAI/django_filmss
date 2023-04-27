from django.shortcuts import render, get_object_or_404

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django_filters.rest_framework import DjangoFilterBackend

from .permissions import IsAuthor

from .models import *
from .serializers import *


class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    # filter_backends = [
    #     filters.OrderingFilter, 
    #     filters.SearchFilter, 
    #     DjangoFilterBackend,
    # ]
    # filterset_fields = ['title', 'year',]
    # search_fields = ['title', 'year',]
    # ordering_fields = ['title', 'year', 'average_rating']


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthor]


@api_view(['GET'])
def toggle_like(request, m_id):
    user = request.user
    movie = get_object_or_404(Movie, id=m_id)

    if Like.objects.filter(user=user, movie=movie).exists():
        Like.objects.filter(user=user, movie=movie).delete()
    else:
        Like.objects.create(user=user, movie=movie)
    
    return Response("Like toggled", 200)


@api_view(['POST'])
def add_rating(request, m_id):
    user = request.user
    movie = get_object_or_404(Movie, id=m_id)
    value = request.POST.get("value")

    if not user.is_authenticated:
        raise ValueError("authentication credentials are not provided")

    if not value:
        raise ValueError("value is required")
    
    if Rating.objects.filter(user=user, movie=movie).exists():
       rating = Rating.objects.get(user=user, movie=movie)
       rating.value = value
       rating.save()
    else:
        Rating.objects.create(user=user, movie=movie, value=value)

    return Response("rating created", 201)


@api_view(['GET'])
def add_to_favorite(request, m_id):
    user = request.user
    movie = get_object_or_404(Movie, id=m_id)

    if Favorite.objects.filter(user=user, movie=movie).exists():
        Favorite.objects.filter(user=user, movie=movie).delete()
        return Response('Deleted from favorite')
    else:
        Favorite.objects.create(user=user, movie=movie, favorited=True)
        return Response('Added to favorites')

class FavoriteView(ListAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated, ]

    def filter_queryset(self, queryset):
        new_queryset = queryset.filter(user=self.request.user)
        return new_queryset