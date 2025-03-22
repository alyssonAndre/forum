from django.shortcuts import render
from quizz.models.Quiz import Question, Alternative
from quizz.models.Base import Course
from collections import Counter

# Create your views here.

def index(request):
    return render(request, 'quizz/index.html')

def careerTest(request):
    return render(request, 'quizz/career_test.html')
