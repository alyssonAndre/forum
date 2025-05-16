from django.shortcuts import render, get_object_or_404
from .models import Post, Comment

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'forum/post_list.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('created_at')
    return render(request, 'forum/post_detail.html', {'post': post, 'comments': comments})
