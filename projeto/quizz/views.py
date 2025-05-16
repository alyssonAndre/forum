from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from quizz.models.Quiz import Question, Alternative
from quizz.models.Base import Course
from collections import Counter

# Create your views here.

def index(request):
    return render(request, 'quizz/index.html')

def careerTest(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'quizz/career_test.html')

def score(request):
    return render(request, 'quizz/score.html')