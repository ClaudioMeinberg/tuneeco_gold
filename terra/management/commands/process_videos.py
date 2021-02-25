from django.core.management.base import BaseCommand, CommandError
from terra.models import Video


class Command(BaseCommand):
    help = 'Download de videos pendentes'

    def handle(self, *args, **options):
        videos = Video.objects.filter(status=Video.Status.APROVADO, processed=False)

        if videos:
            for video in videos:
                video.download()

            self.stdout.write(self.style.SUCCESS('Video List Successfully Processed'))

        else:
            self.stdout.write(self.style.ERROR('Video List Is Empty'))
