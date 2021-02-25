from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from django.contrib.staticfiles import views as static_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from painel import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('', include('painel.urls')),
    path('terra/', include('terra.urls')),
]


if settings.DEBUG:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', static_views.serve),
    ]


admin.site.site_header = 'tuneeco Gold'
