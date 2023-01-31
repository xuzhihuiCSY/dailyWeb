from django import forms
from .models import Album, Song

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['artist', 'album_title', 'A_cover']

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'artist', 'file', 'cover', 'albums']
