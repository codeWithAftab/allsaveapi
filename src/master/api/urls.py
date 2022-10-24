from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('', Home.as_view()),
    path("youtube/",YoutubeAPI.as_view())
]