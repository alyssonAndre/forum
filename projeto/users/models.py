from django.db import models
from django.contrib.auth.models import User
from quizz.models.Base import Course
from quizz.models.SoftDeleteModel import SoftDeleteModel

class UserProfile(SoftDeleteModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    courses = models.ForeignKey(Course, blank=True, null=True, on_delete=models.CASCADE)
    attempts = models.IntegerField(default=0)


    def __str__(self):
        return self.user.username
