from forum.models import *
from django.contrib.auth.models import User


def create_comments():
    user = User.objects.first()
    posts = Post.objects.all()

    for post in posts:
        for i in range(3):
            comment = Comment.objects.create(
                author=user,
                post=post,
                content=f'Este é o conteúdo do comentário de teste número {i+1} no post "{post.title}".',
            )
            print(f'Comentário criado para o post "{post.title}"!')
