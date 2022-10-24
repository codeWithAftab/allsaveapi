from os import stat
from urllib import response
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .utils import get_video_streams
from master.api.apps import ApiConfig
# Create your views here.
class Home(APIView):
    def get(self,request):
        response = {
            "status":200,
            "message":"hello aftab your apis is working correctly."
        }
        return Response(response,status=status.HTTP_200_OK)

class YoutubeAPI(APIView):
    def get(self,request):
        video_id = request.GET.get("video_url","")
        if video_id:
            try:
                response = get_video_streams(video_id)
            except Exception as e:
                return Response(e,status=status.HTTP_400_BAD_REQUEST)

            return Response(response,status=status.HTTP_200_OK)
        
        return Response({
            "status":400,
            "message":"please provide video_url in query params."
        })
        