from django.db import models
from django.contrib.auth.models import User


class Album(models.Model):
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    A_cover = models.ImageField(upload_to='media/covers/', default='media/cover/default.jpg')
    uploader = models.ForeignKey(User, on_delete=models.CASCADE,default='1')

    class Meta:
        ordering = ['album_title']

    def __str__(self):
        return self.album_title

class Song(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    file = models.FileField(upload_to='media/songs/')
    cover = models.ImageField(upload_to='media/covers/', default='media/cover/default.jpg')
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    albums = models.ManyToManyField(Album, related_name='songs', blank=True)
    likes = models.ManyToManyField(User, through='Like', related_name='liked_songs')
    
    def __str__(self):
        return self.title

class Like(models.Model):
    Song = models.ForeignKey(Song, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_private = models.BooleanField(default=True)
