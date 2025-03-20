import os
import django

# Configure a variável de ambiente corretamente para o Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setup.settings")  # ajuste o caminho para o seu arquivo de configurações

# Configure o Django
django.setup()

import json

# Importações absolutas
from quizz.models.Quiz import Quiz, Question, Alternative
from quizz.models.Base import Course  # Caso Course esteja em Base.py

JSON_FILE = "questions.json"  # Ajuste o caminho do arquivo JSON conforme necessário

def carregar_perguntas():
    # Criação ou obtenção do Quiz
    quiz, created = Quiz.objects.get_or_create(
        title="Teste Vocacional de Engenharia",
        description="Descubra qual engenharia combina mais com você!"
    )

    # Carregamento do arquivo JSON
    with open('/app/quizz/questions.json', "r", encoding="utf-8") as file:
        questions_data = json.load(file)  # Aqui você deve carregar os dados do JSON

    # Criação das perguntas e alternativas
    for question_data in questions_data:
        question, _ = Question.objects.get_or_create(quiz=quiz, text=question_data["text"])

        for alt_data in question_data["alternatives"]:
            course = Course.objects.filter(type=alt_data["recommended_course"]).first()

            if course:
                Alternative.objects.get_or_create(
                    question=question,
                    text=alt_data["text"],
                    recommended_course=course,
                    score=alt_data["score"]
                )
            else:
                print(f"Curso {alt_data['recommended_course']} não encontrado para alternativa: {alt_data['text']}")

    print("Perguntas e alternativas importadas com sucesso!")

if __name__ == "__main__":
    carregar_perguntas()
