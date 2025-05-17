from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment

def post_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'forum/post_list.html', {'posts': posts})

def post_detail(request, post_id):
    if not request.user.is_authenticated:
        return redirect('login')
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('created_at')
    return render(request, 'forum/post_detail.html', {'post': post, 'comments': comments})

def post_create(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'forum/post_create.html')
