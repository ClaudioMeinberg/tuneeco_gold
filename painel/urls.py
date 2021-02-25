from django.urls import path, include
from painel import views

urlpatterns = [
    path('', views.root, name='root'),
    path('home', views.home, name='home'),
    path('not_authorized', views.not_authorized, name='not_authorized'),
    path('videos', views.videos, name='videos'),
    path('video/add', views.video_add, name='video_add'),
    path('video/<uuid:pk>/edit', views.video_edit, name='video_edit'),
    path('video/<uuid:pk>', views.video_view, name='video_view'),
]
