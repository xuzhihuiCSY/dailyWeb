from django.urls import path, include,URLPattern
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('login',views.login,name='login'),
    path('user/<int:user_id>',views.user,name='user'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('music_index', views.music_index, name='music_index'),
    path('upload', views.upload_song, name='upload'),
    path('create_album', views.create_album, name='create_album'),
    # start by album_detail/album_title
    path('album_detail/<int:album_id>', views.album_detail, name='album_detail'),
    path('song_detail/<int:song_id>', views.song_detail, name='song_detail'),
    path('song_edit/<int:song_id>', views.song_edit, name='song_edit'),
    # song_delete
    path('song_delete/<int:song_id>', views.song_delete, name='song_delete'),
    # album_edit
    path('album_edit/<int:album_id>', views.album_edit, name='album_edit'),
    # album_delete
    path('album_delete/<int:album_id>', views.album_delete, name='album_delete'),

    path('video_index', views.video_index, name='video_index'),
    path('create_episode', views.create_episode, name='create_episode'),
    path('episode_detail/<int:episode_id>', views.episode_detail, name='episode_detail'),
    path('upload_video/<int:episode_id>', views.upload_video, name='upload_video'),
    path('video_detail/<int:video_id>', views.video_detail, name='video_detail'),
    #video edit
    path('video_edit/<int:video_id>', views.video_edit, name='video_edit'),
    #video delete
    path('video_delete/<int:video_id>', views.video_delete, name='video_delete'),
    #episode edit
    path('episode_edit/<int:episode_id>', views.episode_edit, name='episode_edit'),
    #episode delete
    path('episode_delete/<int:episode_id>', views.episode_delete, name='episode_delete'),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)