from django import forms
from .models import Album, Song

from .models import Episode, Video, VideoComment

class EpisodeForm(forms.ModelForm):
    class Meta:
        model = Episode
        fields = ['title', 'cover', 'description', 'category']

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'file', 'episode_number']

class VideoCommentForm(forms.ModelForm):
    class Meta:
        model = VideoComment
        fields = ['comment']


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['artist', 'album_title', 'A_cover']

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'artist', 'file', 'cover', 'albums']

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)