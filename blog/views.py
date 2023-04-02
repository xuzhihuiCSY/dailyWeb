from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .forms import PostForm, CommentForm

@login_required
def view_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.filter(approved_comment=True)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog:view_post', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/view_post.html', {'post': post, 'comments': comments, 'comment_form': form})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:list_posts')
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})

def list_posts(request):
    posts = Post.objects.order_by('-created_at')
    return render(request, 'blog/list_posts.html', {'posts': posts})

def edit_post(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post.save()
            return redirect('blog:list_posts')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/edit_post.html', {'form': form})

def delete_post(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect('blog:list_posts')

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog:view_post', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blog:view_post', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog:view_post', pk=post_pk)
