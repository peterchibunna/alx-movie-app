"""
URL configuration for AlxMovieApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf.urls.static import static

from main.views import *
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('auth/login', login_view, name='login'),
    path('auth/reset', reset_password, name='reset-password'),
    path('auth/logout', logout, name='logout'),
    path('auth/register', registration, name='register'),
    path('', index, name='index'),
    path('movies', listing, name='movies-list'),
    path('movies/<int:movie_id>', movie_detail, name='movie-detail'),

    path('categories', categories, name='categories'),
]
if settings.DEBUG:
    urlpatterns += [
        re_path(r'^assets/(?P<path>.*)$', serve, {'document_root': settings.ASSETS_ROOT, 'show_indexes': False}),
        # re_path(r'^media/(?P<path>.*)$', protected_serve, {'document_root': settings.MEDIA_ROOT, 'show_indexes': False}),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
