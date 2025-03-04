from django.db import models
from django.contrib.auth.models import User

from quizz.models.Base import Course
from setup.models.SoftDeleteModel import SoftDeleteModel


class Quiz(SoftDeleteModel):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title

class Question(SoftDeleteModel):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()

    def __str__(self):
        return self.text[:50]

class Alternative(SoftDeleteModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='alternatives')
    text = models.TextField()

    recommended_course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.text

class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_answers')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='quiz_answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_answers')
    alternative = models.ForeignKey(Alternative, on_delete=models.CASCADE, related_name='alternative_answers')
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer of {self.user} for {self.question}."



