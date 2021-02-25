import uuid
import os
import shutil
from django.conf import settings
from django.db import models
from pytube import YouTube
import requests


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Feed(BaseModel):
    title = models.CharField(max_length=256)
    link = models.CharField(max_length=256)
    description = models.CharField(max_length=512, null=True, blank=True)
    slug = models.CharField(max_length=256)
    size = models.IntegerField(default=50)
    video_uri = models.CharField(max_length=256)
    thumbnail_uri = models.CharField(max_length=256)

    def __str__(self):
        return '{}'.format(self.title)


class VideoCategory(BaseModel):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=512, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = "video categorie"


class Video(BaseModel):

    class Status(models.TextChoices):
        IDEIA = 'IDEIA', 'Idéia'
        PRODUCAO = 'PRODUCAO', 'Produção'
        REVISAO = 'REVISAO', 'Revisão'
        APROVADO = 'APROVADO', 'Aprovado'
        # PROCESSANDO = 'PROCESSANDO', 'Processando'
        # PUBLICADO = 'PUBLICADO', 'Publicado'
        VIDEO_INVALIDO = 'VIDEO_INVALIDO', 'Vídeo Inválido'

    feed = models.ForeignKey(
        Feed,
        on_delete=models.PROTECT,
        related_name='videos'
    )
    title = models.CharField(max_length=2048, null=True)
    description = models.CharField(max_length=2048, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    article_link = models.CharField(max_length=2048, null=True, blank=True)
    categories = models.ManyToManyField(VideoCategory, blank=True)

    url_youtube_video = models.CharField(max_length=2048, null=True, blank=True)
    url_youtube_thumb = models.CharField(max_length=2048, null=True, blank=True)

    published = models.DateTimeField(null=True, blank=True)

    url_feed_video = models.CharField(max_length=2048, null=True, blank=True)
    url_feed_thumb = models.CharField(max_length=2048, null=True, blank=True)

    video_file_type = models.CharField(max_length=32, default='video/mp4')
    video_duration = models.IntegerField(default=0)

    processed = models.BooleanField(default=False)

    status = models.CharField(max_length=16, choices=Status.choices, default=Status.IDEIA)

    def __str__(self):
        return '{}'.format(self.title)

    def download(self, debug=False):
        try:
            if debug:
                import pdb
                pdb.set_trace()

            if self.url_youtube_video == None or self.url_youtube_video == '':
                return False

            yt = YouTube(self.url_youtube_video)
            self.url_youtube_thumb = yt.thumbnail_url

            output_path = f"{settings.BASE_DIR}/youtube/"

            filename = f"{self.id}"
            thumb_file_ext = yt.thumbnail_url.split('.')[-1]
            path = f"{output_path}{filename}.{thumb_file_ext}"

            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
            }
            response = requests.get(self.url_youtube_thumb, stream=True, headers=headers)

            with open(path, 'wb') as f:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, f)

            video_file_ext = 'mp4'
            stream = yt.streams.filter(
                progressive=True,
                file_extension=video_file_ext
            ).order_by('resolution').desc().first()

            downloaded = stream.download(output_path=output_path, filename=filename)

            self.video_file_type = stream.mime_type
            self.url_feed_video = f"{filename}.{video_file_ext}"
            self.url_feed_thumb = f"{filename}.{thumb_file_ext}"
            self.processed = True

        except:
            self.status = Video.Status.VIDEO_INVALIDO

        finally:
            self.save()

    class Meta:
        ordering = ['published']
