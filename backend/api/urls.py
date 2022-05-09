from django.urls import path

from .views import TestView, AllView, RecentView

urlpatterns = [
    path("test", TestView.as_view()),
    path("all", AllView.as_view()),
    path('recent', RecentView.as_view())
]
