from django.urls import path
from .views import * 

urlpatterns = [
    path('', index, name='index'),
    path('teste-vocacional/', careerTest, name='teste-vocacional'),
]
