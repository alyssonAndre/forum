from django.db import models
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

from quizz.models import Course
from quizz.models.SoftDeleteModel import SoftDeleteModel


def validate_content_length(self, value):
    if len(value) > 5001:
        raise ValidationError('o conteúdo não pode exceder a 5000 caracteres')


class Post(SoftDeleteModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='posts', null=True, blank=True)
    title = models.CharField(max_length=255)
    content = models.TextField(validators=[validate_content_length])
    likes = models.ManyToManyField(User, related_name='like_posts', blank=True)
    dislikes = models.ManyToManyField(User, related_name='dislike_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def like_count(self):
        return self.likes.count()

    def dislike_count(self):
        return self.dislikes.count()

    def __str__(self):
        return f'{self.author} - {self.title}'

class Comment(SoftDeleteModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='like_commnets', blank=True)
    dislikes = models.ManyToManyField(User, related_name='dislike_commnets', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def like_count(self):
        return self.likes.count()

    def dislike_count(self):
        return self.dislikes.count()

    def __str__(self):
        return f'{self.author} - comentou no {self.post}'

