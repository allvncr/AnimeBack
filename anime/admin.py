from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ['name', 'id', 'slug', 'genre_count']
    search_fields = ('name', 'description')


@admin.register(Studio)
class StudioAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ['name', 'id', 'slug', 'studio_count']
    search_fields = ('name',)


class CategoryInline(admin.StackedInline):
    model = Category


@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ['name', 'id', 'studio', 'note', 'date', 'updated', 'episode_count', 'status', 'views']
    list_filter = ['date', 'updated', 'studio', 'genres']
    search_fields = ('name', 'synopsis')
    inlines = [
        CategoryInline
    ]


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ['name', 'id', 'anime', 'views', 'created', 'likes', 'valid']
    list_filter = ['created', 'anime',]
    search_fields = ('name',)