from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.decorators import api_view
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext as _
from rest_framework import serializers, status
from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response

from .models import Channel, Playlist, Account
from .serializers import RegisterSerializer, LoginSerializer, ChannelSerializer, AccountSerializer, PlaylistSerializer

# Create your views here.
User = get_user_model()
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


@api_view(['POST'])
def login(request):
    if request.method == 'POST':

        username = request.data['username']
        password = request.data['password']
        user_obj = User.objects.filter(username=username).first()

        if user_obj is not None:
            credentials = {
                'username': user_obj.username,
                'password': password
            }

            if user_obj.is_active:
                if all(credentials.values()):
                    user = authenticate(**credentials)

                    if user:
                        payload = jwt_payload_handler(user)

                        return Response({
                            "token": jwt_encode_handler(payload),
                            "id": user.id,
                            "username": user.username,
                            "email": user.email
                        }, status=status.HTTP_200_OK)
                    else:
                        msg = _('Impossible de se connecter avec les informations d\'identification fournies.')
                        return Response({
                            "non_field_errors": [msg]
                        }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    msg = _('Doit inclure "username" and "password".')
                    return Response({
                        "non_field_errors": [msg]
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                msg = _('Ce compte utilisateur est désactivé.')
                return Response({
                    "non_field_errors": [msg]
                }, status=status.HTTP_400_BAD_REQUEST)

        else:
            msg = _('Aucun compte avec ce nom d\'utilisateur ')

            return Response({
                "non_field_errors": [msg]
            }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        dataE = serializer.errors

        return Response(dataE, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def channel_list(request):
    if request.method == 'GET':
        channels = get_list_or_404(Channel)

        serializer = ChannelSerializer(channels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def channel_detail(request, username):
    if request.method == 'GET':
        user_obj = User.objects.filter(username=username).first()
        channel = get_object_or_404(Channel, user=user_obj)

        serializer = ChannelSerializer(channel)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def user_list(request):
    if request.method == 'GET':
        users = get_list_or_404(User)

        serializer = AccountSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def user_detail(request, pk):
    if request.method == 'GET':
        user_obj = User.objects.filter(pk=pk).first()

        serializer = AccountSerializer(user_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def playlist_list(request, pk):
    if request.method == 'GET':
        user_obj = get_object_or_404(Account, pk=pk)
        playlists = user_obj.playlists

        serializer = PlaylistSerializer(playlists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
