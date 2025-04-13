from django.urls import path
from .api import *

urlpatterns = [
    path('questions/', QuestionListView.as_view(), name='question-list'),
    path('submit-answers/', SubmitAnswersView.as_view(), name='submit-answers'),
    path('set-chosen-course/', SetChosenCourseView.as_view(), name='set-chosen-course'),
]