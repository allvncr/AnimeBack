from datetime import date
from random import randrange, randint

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *


# Create your views here.

@api_view(['GET'])
def anime_list(request):
    if request.method == 'GET':
        name = request.GET.get('name')
        sort = request.GET.get('sort')

        if name is not None:
            if sort is not None:
                animes = get_list_or_404(Anime.objects.order_by(sort), name__icontains=name)
            else:
                animes = get_list_or_404(Anime, name__icontains=name)
        else:
            animes = get_list_or_404(Anime)
        paginator = Paginator(animes, 12)

        page = request.GET.get('page')

        try:
            animes = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            animes = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999),
            # deliver last page of results.
            animes = paginator.page(paginator.num_pages)

        serializer = AnimeSerializer(animes, many=True)
        data = serializer.data

        return Response({
            "totalItems": paginator.count,
            "list": data
        }, status=status.HTTP_200_OK)



@api_view(['GET'])
def anime_detail(request, pk):
    if request.method == 'GET':
        anime = get_object_or_404(Anime, slug=pk)
        serializer = AnimeSerializer(anime)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def studio_list(request):
    if request.method == 'GET':
        studios = get_list_or_404(Studio)
        serializer = StudioSerializer(studios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def studio_detail(request, pk):
    if request.method == 'GET':
        studio = get_object_or_404(Studio, pk=pk)
        serializer = StudioSerializer(studio)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def genre_list(request):
    if request.method == 'GET':
        genres = get_list_or_404(Genre)
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def genre_detail(request, pk):
    if request.method == 'GET':
        genre = get_object_or_404(Genre, pk=pk)
        serializer = GenreSerializer(genre)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def episodes_all(request):
    if request.method == 'GET':
        episodes = get_list_or_404(Episode, valid=True)
        serializer = EpisodeSerializer(episodes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def episodes_list(request, pk):
    if request.method == 'GET':
        anime = get_object_or_404(Anime, slug=pk)
        episodes = anime.episodes.filter(valid=True)
        serializer = EpisodeSerializer(episodes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def episode_detail(request, pk):
    if request.method == 'GET':
        episode = get_object_or_404(Episode, slug=pk, valid=True)
        Episode.objects.filter(pk=episode.pk).update(views=episode.views+1)
        serializer = EpisodeSerializer(episode)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def random(request):
    if request.method == 'GET':
        animes = get_list_or_404(Anime)
        number = randint(1, len(animes)-1)
        anime = animes[number]

        serializer = AnimeSerializer(anime)
        return Response(serializer.data, status=status.HTTP_200_OK)

