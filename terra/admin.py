from django.contrib import admin

from terra.models import Feed, Video, VideoCategory


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'url_youtube_video',
        'published',
        'processed',
        'status'
    ]
    list_filter = [
        'status',
        'published',
        'processed',
        'feed'
    ]
    search_fields = [
        'title',
        'url_youtube_video',
    ]


@admin.register(VideoCategory)
class VideoCategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'description',
    ]
    list_filter = [
    ]
    search_fields = [
        'name',
        'description',
    ]


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'link',
        'slug',
    ]
    list_filter = [
    ]
    search_fields = [
        'title',
        'link',
        'slug',
        'description',
    ]
