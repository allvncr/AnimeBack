from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from .models import *
from anime.serializers import EpisodeSerializer

from anime.models import Episode


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id',
                  'username',
                  'email',
                  'first_name',
                  'last_name',
                  'date_joined',
                  )


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('username',
                  'password',
                  )
        extra_kwargs = {
            'password': {'write_only': True},
        }


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Account
        fields = ('username',
                  'email',
                  'password',
                  'password2'
                  )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def save(self):
        user = Account(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': ['Les mots de passe doivent correspondre.']})

        user.set_password(password)
        user.save()


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ('id',
                  'description',
                  'location',
                  'views',
                  'photo',
                  'sexe',
                  'created'
                  )


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ('id',
                  'slug',
                  'views')


class PlaylistTrackSerializer(serializers.ModelSerializer):
    track = TrackSerializer()

    class Meta:
        model = PlaylistTrack
        fields = ('id',
                  'track',
                  'position',
                  )


class PlaylistSerializer(serializers.ModelSerializer):
    tracks = PlaylistTrackSerializer(
        many=True
    )


    class Meta:
        model = Playlist
        fields = ('id',
                  'name',
                  'user',
                  'created',
                  'updated',
                  'tracks',
                  )
