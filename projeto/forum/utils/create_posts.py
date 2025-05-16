from forum.models import Post
from django.contrib.auth.models import User
from quizz.models import Course

def create_posts():
    user = User.objects.first()
    course = Course.objects.first()

    for i in range(10):
        post = Post.objects.create(
            author=user,
            course=course,
            title=f'Post de Teste {i+1}',
            content=f'Este é o conteúdo do post de teste número {i+1}.',
        )
        print(f'Post "{post.title}" criado com sucesso!')