from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from .models import Album, Song,Like
from .forms import SongForm,AlbumForm
from django.contrib.auth.models import User

import json
import urllib.request

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
                return redirect('index')
            else:
                messages.info(request,'Credentials Invalid')
                return redirect('login')
        elif request.POST.get('submit') == 'signUp':
            # your sign up
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['password2']

            if password == password2:
                if User.objects.filter(email=email).exists():
                    messages.info(request,'Email Used')
                    return redirect('login')
                elif User.objects.filter(username=username).exists():
                    messages.info(request,'Username Used')
                    return redirect('login')
                else:
                    user = User.objects.create_user(username=username,email=email,password=password)
                    user.save()
                    auth.login(request,user)
                    return redirect('index')
            else:
                messages.info(request,'Password Not the Same')
                return redirect('login')
    else:
        return render(request,'login.html')


def upload_song(request):
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            album_list = form.cleaned_data['albums']
            # Save the song object and assign the selected albums to it
            song = form.save(commit=False)
            song.uploader = request.user
            song.save()
            song.albums.set(album_list)
            song.save()
            return redirect('music_index')
    else:
        form = SongForm()
    return render(request, 'music/music_upload.html', {'form': form})

def music_index(request):
    query = request.GET.get('q')
    if query:
        albums = Album.objects.filter(album_title__icontains=query)
        songs = Song.objects.filter(title__icontains=query)
    else:
        albums = Album.objects.all()
        songs = Song.objects.all()
    return render(request, 'music/music_index.html', {'albums': albums, 'songs': songs})

def create_album(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('music_index')
    else:
        form = AlbumForm()
    return render(request, 'music/create_album.html', {'form': form})

def album_detail(request, album_id):
    album_id = album_id
    album = Album.objects.get(id=album_id)
    #get songs that have the Album as model
    songs = Song.objects.filter(albums=album_id)
    return render(request, 'music/album_detail.html', {'album': album, 'songs': songs})

def like_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    Like.objects.create(user=request.user, song=song)
    return redirect('music/song_detail', song_id=song_id)

def unlike_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    Like.objects.filter(user=request.user, song=song).delete()
    return redirect('music/song_detail', song_id=song_id)

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
    
    context = {
        'song': song,
        'is_liked': is_liked,
    }

    return render(request, 'music/song_detail.html', context)


#song edit or delete page
def song_edit(request, song_id):
    song = Song.objects.get(id=song_id)
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES, instance=song)
        if form.is_valid():
            form.save()
            return redirect('music_index')
    else:
        form = SongForm(instance=song)
    return render(request, 'music/song_edit.html', {'form': form})

#song delete confirm page
def song_delete(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    if request.method == 'POST':
        song.delete()
        return redirect('music_index')
    return render(request, 'music/song_delete.html', {'song': song})

#album edit
def album_edit(request, album_id):
    album = Album.objects.get(id=album_id)
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES, instance=album)
        if form.is_valid():
            form.save()
            return redirect('music_index')
    else:
        form = AlbumForm(instance=album)
    return render(request, 'music/album_edit.html', {'form': form})

#album delete
def album_delete(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    if request.method == 'POST':
        album.delete()
        return redirect('music_index')
    return render(request, 'music/album_delete.html', {'album': album})


def user(request, user_id):
    user = User.objects.get(id=user_id)
    albums = Album.objects.filter(uploader=user_id)
    songs = Song.objects.filter(uploader=user_id)
    likes = Like.objects.filter(user=user_id)
    return render(request, 'user.html', {'user': user, 'albums': albums, 'songs': songs, 'likes': likes})