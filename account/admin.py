from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ['user', 'id', 'location', 'created']


class PlaylistInline(admin.TabularInline):
    model = PlaylistTrack


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'created', 'updated', 'user']
    list_filter = ['created', 'updated', 'user']
    search_fields = ('name',)
    inlines = [
        PlaylistInline
    ]


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['username', 'id', 'email', 'date_joined', 'is_superuser', 'last_login', 'is_active']
    list_filter = ['date_joined', 'last_login', 'is_active']
    search_fields = ('username', 'email')
    ordering = ('date_joined',)
