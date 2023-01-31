from django.contrib import admin
from .models import Album, Song, Like

admin.site.register(Album)
admin.site.register(Song)
admin.site.register(Like)