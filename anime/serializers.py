from rest_framework.serializers import *
from .models import *


class GenreSerializer(ModelSerializer):
    total = SerializerMethodField()

    class Meta:
        model = Genre
        fields = [
            'id',
            'name',
            'slug',
            'image',
            'description',
            'total'
        ]

    def get_total(self, obj):
        return obj.genre_count


class StudioSerializer(ModelSerializer):
    total = SerializerMethodField()

    class Meta:
        model = Studio
        fields = [
            'id',
            'name',
            'slug',
            'total'
        ]

    def get_total(self, obj):
        return obj.studio_count


class AnimeSerializer(ModelSerializer):
    studio = StudioSerializer(
        required=True
    )
    genres = GenreSerializer(
        required=True,
        many=True
    )
    total = SerializerMethodField()

    class Meta:
        model = Anime
        fields = [
            'id',
            'name',
            'slug',
            'genres',
            'studio',
            'image',
            'date',
            'note',
            'status',
            'synopsis',
            'total',
            'views'
        ]

    def get_total(self, obj):
        return obj.episode_count


class EpisodeSerializer(ModelSerializer):
    anime = AnimeSerializer(
        required=True
    )

    class Meta:
        model = Episode
        fields = [
            'id',
            'name',
            'slug',
            'anime',
            'updated',
            'views',
            'likes',
            'dislike',
            'video',
            'download'
        ]
