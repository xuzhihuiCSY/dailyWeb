# urls.py

from django.urls import path
from . import views



app_name = 'blog'


urlpatterns = [
    path('', views.list_posts, name='list_posts'),
    path('create/', views.create_post, name='create_post'),
    path('<int:pk>/', views.view_post, name='view_post'),
    path('<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('<int:pk>/delete/', views.delete_post, name='delete_post'),
    # URLs for comments
    path('<int:pk>/comments/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comments/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    path('comments/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
    ]