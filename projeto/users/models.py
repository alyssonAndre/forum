from django.db import models
from django.contrib.auth.models import User

from forum.models import Post
from quizz.models.Base import Course
from quizz.models.SoftDeleteModel import SoftDeleteModel

class UserProfile(SoftDeleteModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    courses = models.ForeignKey(Course, blank=True, null=True, on_delete=models.CASCADE)
    attempts = models.IntegerField(default=0)


    def __str__(self):
        return self.user.username

    @property
    def total_posts(self):
        return Post.objects.filter(author=self.user, is_deleted=False).count()

    @property
    def total_likes_given(self):
        post_likes = self.user.like_posts.count()
        comment_likes = self.user.like_commnets.count()
        return post_likes + comment_likes

    @property
    def total_dislikes_given(self):
        post_dislikes = self.user.dislike_posts.count()
        comment_dislikes = self.user.dislike_commnets.count()
        return post_dislikes + comment_dislikes