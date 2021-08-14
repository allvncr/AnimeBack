from django.urls import path
from . import views


urlpatterns = [

    path('anime/random/', views.random,
         name='anime_random'),

    path('anime/all/', views.anime_list,
         name='anime_list'),

    path('anime/<slug:pk>/', views.anime_detail,
         name='anime_detail'),

    path('genre/all/', views.genre_list,
         name='genre_list'),

    path('genre/<int:pk>/', views.genre_detail,
         name='genre_detail'),

    path('studio/all/', views.studio_list,
         name='studio_list'),

    path('studio/<int:pk>/', views.studio_detail,
         name='studio_detail'),

    path('episode/all/', views.episodes_all,
         name='episode_all'),

    path('anime/<slug:pk>/episode/all/', views.episodes_list,
         name='anime_episode_list'),

    path('episode/<slug:pk>/', views.episode_detail,
         name='episode_detail'),

]