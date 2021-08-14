from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    path('channel/all/', views.channel_list,
         name='channel_list'),
    path('channel/<str:username>/', views.channel_detail,
         name='channel_detail'),
    path('user/all/', views.user_list,
         name='user_list'),
    path('user/<int:pk>/', views.user_detail,
         name='user_detail'),
    path('user/<int:pk>/playlist/all', views.playlist_list,
         name='playlist_list'),
]
