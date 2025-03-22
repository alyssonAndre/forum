from django.urls import path
from .api import QuestionListView

urlpatterns = [
    path('questions/', QuestionListView.as_view(), name='question-list'),
]