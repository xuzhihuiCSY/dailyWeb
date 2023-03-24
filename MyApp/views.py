from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from .models import Album, Song,Like,Episode, Video, VideoComment
from .forms import SongForm,AlbumForm,EpisodeForm, VideoForm, VideoCommentForm
from django.contrib.auth.models import User
from newsapi import NewsApiClient
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from django.db.models.signals import post_save
from django.dispatch import receiver

import os
import requests
import json
import urllib.request
from urllib.error import HTTPError
from ecommerce.models import Order
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.urls import reverse_lazy
from To_Do_List.models import Task

@user_passes_test(lambda u: u.is_authenticated, login_url=reverse_lazy('MyApp:login'))
def more_list(request):
    if not request.user.is_authenticated:
        messages.info(request, 'Please log in to use this feature.')
    return render(request, 'more/more_list.html')

# Create your views here.

def index(request):
    return render(request, 'index.html')

def login(request):
    
    if request.method == "POST":
        if request.POST.get('submit') == 'login':
            # your sign in logic goes here
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username,password=password)

            if user is not None:
                auth.login(request,user)
                return redirect('MyApp:index')
            else:
                messages.info(request,'Credentials Invalid')
                return redirect('MyApp:login')
        elif request.POST.get('submit') == 'signUp':
            # your sign up
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['password2']

            if password == password2:
                if User.objects.filter(email=email).exists():
                    messages.info(request,'Email Used')
                    return redirect('MyApp:login')
                elif User.objects.filter(username=username).exists():
                    messages.info(request,'Username Used')
                    return redirect('MyApp:login')
                else:
                    user = User.objects.create_user(username=username,email=email,password=password)
                    user.save()
                    auth.login(request,user)
                    return redirect('MyApp:index')
            else:
                messages.info(request,'Password Not the Same')
                return redirect('MyApp:login')
    else:
        return render(request,'login.html')

@user_passes_test(lambda u: u.is_authenticated, login_url=reverse_lazy('MyApp:login'))
def upload_song(request):
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            album_list = form.cleaned_data['albums']
            song = form.save(commit=False)
            song.uploader = request.user
            song.save()
            song.albums.set(album_list)
            return redirect('MyApp:music_index')
    else:
        form = SongForm()
    return render(request, 'music/music_upload.html', {'form': form})

@receiver(post_save, sender=Song)
def set_default_cover(sender, instance, created, **kwargs):
    if created and not instance.cover:
        instance.cover.name = os.path.join(settings.MEDIA_ROOT, 'cover', 'default.jpg')
        instance.save()

def music_index(request):
    query = request.GET.get('q')
    if query:
        albums = Album.objects.filter(album_title__icontains=query)
        songs = Song.objects.filter(title__icontains=query)
    else:
        albums = Album.objects.all()
        songs = Song.objects.all()
    return render(request, 'music/music_index.html', {'albums': albums, 'songs': songs})

@user_passes_test(lambda u: u.is_authenticated, login_url=reverse_lazy('MyApp:login'))
def create_album(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('MyApp:music_index')
    else:
        form = AlbumForm()
    return render(request, 'music/create_album.html', {'form': form})

def album_detail(request, album_id):
    album = Album.objects.get(id=album_id)
    songs = Song.objects.filter(albums=album_id)
    context = {'album': album, 'songs': songs}
    return render(request, 'music/album_detail.html', context)

def like_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    Like.objects.create(user=request.user, song=song)
    return redirect('music/song_detail', song_id=song_id)

def unlike_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    Like.objects.filter(user=request.user, song=song).delete()
    return redirect('music/song_detail', song_id=song_id)

# liked song list page
@user_passes_test(lambda u: u.is_authenticated, login_url=reverse_lazy('MyApp:login'))
def liked_song_list(request):
    user = request.user
    liked_songs = Like.objects.filter(user=user)
    context = {
        'liked_songs': liked_songs,
    }
    return render(request, 'music/liked_song_list.html', context)

def song_detail(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    user = request.user
    is_liked = False

    if request.method == 'POST':
        like, created = Like.objects.get_or_create(Song=song, user=user)
        if not created:
            like.delete()
            is_liked = False
        else:
            is_liked = True
    if request.user.is_authenticated:
        if Like.objects.filter(Song=song, user=request.user).exists():
            is_liked = True
    context = {
        'song': song,
        'is_liked': is_liked,
    }

    return render(request, 'music/song_detail.html', context)


#song edit or delete page
@user_passes_test(lambda u: u.is_authenticated, login_url=reverse_lazy('MyApp:login'))
def song_edit(request, song_id):
    song = Song.objects.get(id=song_id)
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES, instance=song)
        if form.is_valid():
            form.save()
            return redirect('MyApp:user', user_id=request.user.id)
    else:
        form = SongForm(instance=song)
    return render(request, 'music/song_edit.html', {'form': form})

#song delete confirm page
@user_passes_test(lambda u: u.is_authenticated, login_url=reverse_lazy('MyApp:login'))
def song_delete(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    if request.method == 'POST':
        song.delete()
        return redirect('MyApp:user', user_id=request.user.id)
    return render(request, 'music/song_delete.html', {'song': song})

#album edit
@user_passes_test(lambda u: u.is_authenticated, login_url=reverse_lazy('MyApp:login'))
def album_edit(request, album_id):
    album = Album.objects.get(id=album_id)
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES, instance=album)
        if form.is_valid():
            form.save()
            return redirect('MyApp:user', user_id=request.user.id)
    else:
        form = AlbumForm(instance=album)
    return render(request, 'music/album_edit.html', {'form': form})

#album delete
@user_passes_test(lambda u: u.is_authenticated, login_url=reverse_lazy('MyApp:login'))
def album_delete(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    if request.method == 'POST':
        album.delete()
        return redirect('MyApp:user', user_id=request.user.id)
    return render(request, 'music/album_delete.html', {'album': album})

def video_index(request):
    query = request.GET.get('q')
    if query:
        episodes = Episode.objects.filter(title__icontains=query)
        videos = Video.objects.filter(title__icontains=query)
    else:
        episodes = Episode.objects.all()
        videos = Video.objects.all()
    return render(request, 'video/video_index.html', {'episodes':episodes,'videos':videos})

def create_episode(request):
    if request.method == 'POST':
        form = EpisodeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('MyApp:video_index')
    else:
        form = EpisodeForm()

    return render(request, 'video/create_episode.html', {'form':form})

def upload_video(request, episode_id):
    episode = get_object_or_404(Episode, pk=episode_id)
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.uploader = request.user
            video.save()
            video.episode.set([episode])
            return redirect('MyApp:video_index')
    else:
        form = VideoForm()
    return render(request, 'video/upload_video.html', {'form':form})

def episode_detail(request, episode_id):
    episode = get_object_or_404(Episode, pk=episode_id)
    videos = Video.objects.filter(episode=episode)
    context = {
        'episode': episode,
        'videos': videos,
    }
    return render(request, 'video/episode_detail.html', context)

def video_detail(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    comments = VideoComment.objects.filter(video=video)
    videos_in_same_episode = Video.objects.filter(episode=video.episode.first())
    if request.method == 'POST':
        form = VideoCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.video = video
            comment.user = request.user
            comment.save()
            return redirect('MyApp:video_detail', video_id)
    else:
        form = VideoCommentForm()
    context = {
        'video': video,
        'comments': comments,
        'videos_in_same_episode': videos_in_same_episode,
        'form': form,
    }
    return render(request, 'video/video_detail.html', context)

def episode_delete(request, episode_id):
    episode = get_object_or_404(Episode, pk=episode_id)
    if request.method == 'POST':
        episode.delete()
        return redirect('MyApp:user', user_id=request.user.id)
    return render(request, 'video/episode_delete.html', {'episode':episode})

def video_delete(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    if request.method == 'POST':
        video.delete()
        return redirect('MyApp:user', user_id=request.user.id)
    return render(request, 'video/video_delete.html', {'video':video})

def episode_edit(request, episode_id):
    episode = get_object_or_404(Episode, pk=episode_id)
    if request.method == 'POST':
        form = EpisodeForm(request.POST, request.FILES, instance=episode)
        if form.is_valid():
            form.save()
            return redirect('MyApp:user', user_id=request.user.id)
    else:
        form = EpisodeForm(instance=episode)
    return render(request, 'video/episode_edit.html', {'form':form})

def video_edit(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            return redirect('MyApp:user', user_id=request.user.id)
    else:
        form = VideoForm(instance=video)
    return render(request, 'video/video_edit.html', {'form':form})

def user(request, user_id):
    user = User.objects.get(id=user_id)
    albums = Album.objects.filter(uploader=user_id)
    songs = Song.objects.filter(uploader=user_id)
    likes = Like.objects.filter(user=user_id)
    episodes = Episode.objects.filter(uploader=user)
    videos = Video.objects.filter(uploader=user)
    orders = Order.objects.filter(user=user_id)
    tasks = Task.objects.filter(user=user_id, complete=False)
    return render(request, 'user.html', {'user': user, 'albums': albums, 'songs': songs, 
                                         'likes': likes, 'episodes': episodes, 'videos': videos,
                                         'orders': orders,'tasks': tasks})

def news_page(request):
    if 'query' in request.GET:
        query = request.GET['query']
        newsapi = NewsApiClient(api_key='6a8d8580dafd470f84f941c96205627e')
        all_articles = newsapi.get_everything(q=query, sources='bbc-news,the-verge')
        articles = all_articles['articles']
    else:
        newsapi = NewsApiClient(api_key='6a8d8580dafd470f84f941c96205627e')
        top_headlines = newsapi.get_top_headlines(sources='bbc-news,the-verge')
        articles = top_headlines['articles']
    desc = []
    news = []
    img = []
    for i in range(len(articles)):
        myarticles = articles[i]
        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])
    mylist = zip(news, desc, img)
    return render(request, 'news/news.html', context={"mylist":mylist})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            send_mail(
                f"{subject} from {name} ({email})",
                message,
                email,
                [settings.DEFAULT_FROM_EMAIL],
            )
            # go back to index page
            return redirect('MyApp:index')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def weather(request):
    if request.method == 'POST':
        city = request.POST['city']
        try:
            res = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q='+city+'&appid=cb771e45ac79a4e8e2205c0ce66ff633').read()
            json_data = json.loads(res)
        except HTTPError as e:
            if e.code == 404:
                data = {'city_not_found': True}
                return render(request, 'more/weather.html', {'city': city, 'data': data})
            else:
                raise e
        else:
            temp_k = float(json_data['main']['temp'])
            temp_c = round(temp_k - 273.15, 2)
            data = {
                "country_code": str(json_data['sys']['country']),
                "coordinate": str(json_data['coord']['lon']) + ' ' + str(json_data['coord']['lat']),
                "temp": str(temp_c) + ' °C',
                "pressure": str(json_data['main']['pressure'])+' hPa',
                "humidity": str(json_data['main']['humidity']),
                "weather": str(json_data['weather'][0]['main']),
                "weather_icon": get_weather_icon(json_data['weather'][0]['main']),
                "id": str(json_data['weather'][0]['id']),
                "feels_like": str(round(float(json_data['main']['feels_like']) - 273.15, 2))+' °C',
                "cod": str(json_data['cod']),
            }
    else:
        city = ''
        data = {}
    return render(request, 'more/weather.html', {'city': city, 'data': data})

def get_weather_icon(weather):
    if weather == 'Clear':
        return '<i class="fas fa-sun"></i>'
    elif weather == 'Few clouds':
        return '<i class="fas fa-cloud-sun"></i>'
    elif weather == 'Clouds' or weather == 'Broken clouds':
        return '<i class="fas fa-cloud"></i>'
    elif weather == 'Shower rain':
        return '<i class="fas fa-cloud-showers-heavy"></i>'
    elif weather == 'Rain':
        return '<i class="fas fa-cloud-rain"></i>'
    elif weather == 'Thunderstorm':
        return '<i class="fas fa-bolt"></i>'
    elif weather == 'Snow':
        return '<i class="fas fa-snowflake"></i>'
    elif weather == 'Mist':
        return '<i class="fas fa-smog"></i>'
    else:
        return ''

def chess(request):
    pieces = ['wK', 'bK', 'wQ', 'bQ', 'wR', 'bR', 'wB', 'bB', 'wN', 'bN', 'wP', 'bP']
    context = {
        'pieces': pieces
    }
    return render(request, 'more/chess.html', context)

def wheel(request):
    return render(request, 'more/wheel.html')

