from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Task
from django.contrib.auth.models import User,auth

# Create your views here.
class TaskList(ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'tasks/task_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user.id)
        context['count'] = context['tasks'].filter(complete=False).count()
        
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__contains=search_input)

        context['search_input'] = search_input

        return context

class TaskDetail(DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'tasks/task.html'

class TaskCreate(CreateView):
    model = Task
    fields = {'title','description','complete'}
    success_url = reverse_lazy('To_Do_List:tasks')
    template_name = 'tasks/task_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate,self).form_valid(form)

class TaskUpdate(UpdateView):
    model = Task
    fields = {'title','description','complete'}
    success_url = reverse_lazy('To_Do_List:tasks')
    template_name = 'tasks/task_update.html'

class DeleteView(DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('To_Do_List:tasks')
    template_name = 'tasks/task_delete.html'