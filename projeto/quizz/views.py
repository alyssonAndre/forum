from django.shortcuts import render
from quizz.models.Quiz import Question, Alternative
from quizz.models.Base import Course
from collections import Counter

# Create your views here.

def index(request):
    return render(request, 'quizz/index.html')

def careerTest(request):
    if request.method == 'POST':
        career_count = Counter()

    for key, value in request.POST.items():
        if key.startswith('question_') and value:
            try:
                career_id = int(value)
                career_count[career_id] += 1
            except ValueError:
                continue

        if career_count:
            most_common_career_id, _ = career_count.most_common(1)[0]
            most_common_career = Course.objects.get(id=most_common_career_id)
            return render(request, 'quizz/index.html', {'career': most_common_career})


    questions = Question.objects.order_by('?')[:10]  # Pega 10 perguntas aleatórias
    return render(request, 'quizz/career_test.html', {'questions': questions})
