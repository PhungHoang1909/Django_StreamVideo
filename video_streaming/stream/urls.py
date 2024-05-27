from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('video_feed/<str:stream_id>/', views.stream_video, name='video_feed'),
]
