from django import forms
from ckeditor.widgets import CKEditorWidget

from terra.models import Video


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = [
            'feed',
            'title',
            'description',
            'content',
            'article_link',
            'categories',
            'url_youtube_video',
            'published',
            'status'
        ]
        widgets = {
            'feed': forms.Select(attrs={'class': 'form-control', 'data-msg': 'Preenchimento obrigatório'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'data-msg': 'Preenchimento obrigatório', 'autocomplete': 'off'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'data-msg': 'Preenchimento obrigatório', 'autocomplete': 'off'}),
            'content': CKEditorWidget(attrs={'data-msg': 'Preenchimento obrigatório'}),
            'article_link': forms.TextInput(attrs={'class': 'form-control', 'data-msg': 'Preenchimento obrigatório', 'autocomplete': 'off'}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-control', 'data-msg': 'Preenchimento obrigatório'}),
            'url_youtube_video': forms.TextInput(attrs={'class': 'form-control', 'data-msg': 'Preenchimento obrigatório', 'autocomplete': 'off'}),
            'published': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input', 'data-target': '#datetimepicker1'}),
        }
