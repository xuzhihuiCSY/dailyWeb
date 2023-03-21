from . import views
from .views import TaskCreate, TaskList,TaskDetail,TaskCreate,TaskUpdate,DeleteView
from django.conf import settings
from django.urls import URLPattern, path

app_name='To_Do_List'

urlpatterns = [
    path('tasks',TaskList.as_view(),name='tasks'),
    path('task/<int:pk>/',TaskDetail.as_view(),name='task'),
    path('task-create/',TaskCreate.as_view(),name='task-create'),
    path('task-update/<int:pk>/',TaskUpdate.as_view(),name='task-update'),
    path('task-delete/<int:pk>/',DeleteView.as_view(),name='task-delete'),
 ]
