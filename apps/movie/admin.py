from django.contrib import admin

from .models import Genre, Movie, Comment, Rating, Like, Favorite


admin.site.register([Genre, Movie, Comment, Rating, Like, Favorite])