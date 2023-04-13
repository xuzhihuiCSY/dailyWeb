from django.urls import path

from . import views

urlpatterns = [
    path("", views.Cindex, name="Cindex"),
    path("<str:room_name>/", views.room, name="room"),
    
]