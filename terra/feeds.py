from django.contrib.syndication import views
from terra.models import Video, Feed
from django.utils.feedgenerator import Rss201rev2Feed
from django.utils import timezone
from django.utils.safestring import mark_safe
from html.parser import HTMLParser

unescape = HTMLParser().unescape


class TerraVideoFeed(Rss201rev2Feed):
    def rss_attributes(self):
        attrs = super().rss_attributes()

        attrs['xmlns:media'] = 'http://search.yahoo.com/mrss/'
        attrs['xmlns:content'] = 'http://purl.org/rss/1.0/modules/content/'

        return attrs

    def add_item_elements(self, handler, item):
        super().add_item_elements(handler, item)

        content = item['content']
        handler.startElement('content:encoded', {})
        handler._write(f'<![CDATA[ {content} ]]>')
        handler.endElement('content:encoded')

        video = dict(url=item['url_feed_video'])
        video['type'] = item['video_file_type']
        video['duration'] = item['video_duration']
        video['medium'] = 'video'

        handler.startElement("media:content", video)

        thumbnail = dict(url=item['url_feed_thumb'])
        handler.addQuickElement('media:thumbnail', '', thumbnail)

        handler.endElement("media:content")

    def root_attributes(self):
        attrs = super().root_attributes()

        return attrs

    def add_root_elements(self, handler):
        super().add_root_elements(handler)


class LatestVideosFeed(views.Feed):

    feed_type = TerraVideoFeed

    def get_object(self, request, slug, item_id=None):
        feed = Feed.objects.get(slug=slug)
        self.title = feed.title
        self.link = feed.link
        self.description = feed.description

        return feed

    def items(self, feed):
        return Video.objects.filter(
            processed=True,
            published__lt=timezone.now(),
            feed=feed,
            status=Video.Status.APROVADO
        ).order_by('-published')[:feed.size]

    def item_title(self, item):
        return item.title

    def item_link(self, item):
        return item.article_link

    def item_guid(self, item):
        return item.id

    def item_guid_is_permalink(self, obj):
        pass

    item_guid_is_permalink = False

    def item_description(self, item):
        return item.description

    def item_categories(self, item):
        return item.categories.all()

    def item_pubdate(self, item):
        return item.published

    def item_extra_kwargs(self, item):
        thumb_url = f'{item.feed.thumbnail_uri}{item.url_feed_thumb}'
        thumb_str = f'<img src="{thumb_url}" style="display:none; ">'
        content = f'{item.content}{thumb_str}'
        return {
            'url_feed_video': f'{item.feed.video_uri}{item.url_feed_video}',
            'url_feed_thumb': thumb_url,
            'video_file_type': item.video_file_type,
            'video_duration': str(item.video_duration),
            'content': content,
        }
