from django.shortcuts import render
from werkzeug import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response

import firebase_admin
from firebase_admin import credentials, messaging
from .models import Snap
from .serializers import SnapSerializer

# Create your views here.


class TestView(APIView):
    def get(self, request, format=None):
        return Response({"message": "Hello from the other side 🗢", "data": "fuck you", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/330px-Image_created_with_a_mobile_phone.png"}, status=status.HTTP_200_OK)

class AllView(generics.ListAPIView):
    queryset = Snap.objects.all()
    serializer_class = SnapSerializer

class RecentView(generics.ListAPIView):
    queryset = Snap.objects.all().order_by('-time')[:10]
    serializer_class = SnapSerializer



# default_app = firebase_admin.initialize_app()

