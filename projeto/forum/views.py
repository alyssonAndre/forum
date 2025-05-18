from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.utils import timezone
from .forms import PostCreateForm
from .models import Post, Comment

def post_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    today = timezone.now().date()
    profile = request.user.profile

    if profile.last_attempt_date != today:
        profile.attempts = 0
        profile.last_attempt_date = today
        profile.save()


    quiz_attempts = profile.attempts >=3

    posts = Post.objects.all().order_by('-created_at')

    return render(request, 'forum/post_list.html', {'posts': posts, 'quiz_attempts': quiz_attempts})



def post_detail(request, post_id):
    if not request.user.is_authenticated:
        return redirect('login')
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-created_at')
    return render(request, 'forum/post_detail.html', {'post': post, 'comments': comments})


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'forum/post_create.html'
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Post criado e publicado com sucesso!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'post_id': self.object.id})