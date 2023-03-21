from django.db import models
from django.contrib.auth.models import User


class Album(models.Model):
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    A_cover = models.ImageField(upload_to='Song_covers/', default='Song_cover/default.jpg')
    uploader = models.ForeignKey(User, on_delete=models.CASCADE,default='1')

    class Meta:
        ordering = ['album_title']

    def __str__(self):
        return self.album_title

class Song(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    file = models.FileField(upload_to='songs/')
    cover = models.ImageField(upload_to='Song_covers/', default='Song_cover/default.jpg')
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    albums = models.ManyToManyField(Album, related_name='songs', blank=True)
    likes = models.ManyToManyField(User, through='Like', related_name='liked_songs')
    
    def __str__(self):
        return self.title

class Like(models.Model):
    Song = models.ForeignKey(Song, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_private = models.BooleanField(default=True)


class Episode(models.Model):
    ANIME = 'Anime'
    TV_SERIES = 'TV Series'
    MOVIES = 'Movies'
    DOCUMENTARIES = 'Documentaries'
    CATEGORY_CHOICES = (
        (ANIME, 'Anime'),
        (TV_SERIES, 'TV Series'),
        (MOVIES, 'Movies'),
        (DOCUMENTARIES, 'Documentaries'),
    )
    title = models.CharField(max_length=500)
    cover = models.ImageField(upload_to='episode_covers/', default='episode_covers/default.jpg')
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    description = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default=MOVIES)
    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title 

class Video(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='videos/')
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    episode = models.ManyToManyField(Episode, related_name='videos', blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    episode_number = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ['episode_number']

    def __str__(self):
        return self.title

class VideoComment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.comment
