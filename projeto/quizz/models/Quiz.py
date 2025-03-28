from collections import defaultdict
from django.db import models
from django.contrib.auth.models import User

from quizz.models.Base import Course
from quizz.models.SoftDeleteModel import SoftDeleteModel


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


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @classmethod
    def calculate_score(cls, user, quiz):
        user_answers = cls.objects.filter(user=user, quiz=quiz)
        course_scores = defaultdict(int)

        for answer in user_answers:
            if answer.alternative.recommended_course:
                course_scores[answer.alternative.recommended_course] += answer.alternative.score

        if not course_scores:
            return None, 0

        max_score = max(course_scores.values())
        best_courses = [course for course, score in course_scores.items() if score == max_score]

        if len(best_courses) == 1:
            return best_courses[0], max_score
        else:
            return best_courses, max_score