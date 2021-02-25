from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q
from terra.models import Video
from terra.forms import VideoForm

# Create your views here.


def login(request):
    return render(request, 'login/login.html')


@login_required
def root(request):
    # return redirect('home')
    return redirect('videos')


@login_required
def home(request):
    return render(request, 'login/home.html')


@login_required
def not_authorized(request):
    return render(request, '401.html')


@login_required
@permission_required('terra.view_video', 'not_authorized')
def videos(request):

    data = {
        'videos_em_producao': Video.objects.filter(~Q(status=Video.Status.APROVADO)),
        'videos_processando': Video.objects.filter(status=Video.Status.APROVADO, processed=False),
        'videos_agendados': Video.objects.filter(status=Video.Status.APROVADO, processed=True, published__gt=timezone.now()),
        'videos_publicados': Video.objects.filter(status=Video.Status.APROVADO, processed=True, published__lte=timezone.now()),
    }

    return render(request, 'feed/videos.html', data)


@login_required
@permission_required('terra.add_video', 'not_authorized')
def video_add(request, template_name='feed/video_form.html'):
    form = VideoForm(request.POST or None)
    if form.is_valid():
        form.save()

        messages.success(request, 'Item incluído com sucesso!')

        return redirect('videos')
    return render(request, template_name, {'form': form})


@login_required
@permission_required('terra.change_video', 'not_authorized')
def video_edit(request, pk, template_name='feed/video_form.html'):
    video = get_object_or_404(Video, pk=pk)
    form = VideoForm(request.POST or None, instance=video)

    if request.POST.get('status') in [Video.Status['REVISAO'], Video.Status['APROVADO']]:
        form.fields['description'].required = True
        form.fields['categories'].required = True
        form.fields['url_youtube_video'].required = True

    if request.POST.get('status') == Video.Status['APROVADO']:
        form.fields['article_link'].required = True
        form.fields['published'].required = True

    if form.is_valid():
        form.save()

        messages.success(request, 'Item atualizado com sucesso!')

        return redirect('videos')
    return render(request, template_name, {'form': form})


@login_required
@permission_required('terra.view_video', 'not_authorized')
def video_view(request, pk, template_name='feed/video.html'):
    video = get_object_or_404(Video, pk=pk)

    return render(request, template_name, {'video': video})
