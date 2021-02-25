from django.urls import path
from django.conf.urls import url

from terra import views

from .feeds import LatestVideosFeed


urlpatterns = [
    path("<str:slug>/feed/video", LatestVideosFeed(), name="video_feed"),
    path("<str:slug>/feed/video/<str:item_id>", LatestVideosFeed(), name="video_feed_id"),
]
