from django.contrib import admin
from .models import Album, Song, Like, Episode, Video, VideoComment

admin.site.register(Album)
admin.site.register(Song)
admin.site.register(Like)
admin.site.register(Episode)
admin.site.register(Video)
admin.site.register(VideoComment)
