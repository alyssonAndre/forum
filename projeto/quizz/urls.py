from django.urls import path
from .views import * 

urlpatterns = [
    path('', index, name='index'),
    path('teste-vocacional/', careerTest, name='teste-vocacional'),
    path('score/', score, name='score'),
]
