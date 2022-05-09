from django.urls import path

# from .views import TestView
from .apps import index


urlpatterns = [
    path("test", index, name='webcam_feed'),
]
