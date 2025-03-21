import os
import django
import json

# Configurar Django antes de importar modelos
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setup.settings")
django.setup()

# Importações absolutas dos modelos
from quizz.models.Quiz import Quiz, Question, Alternative
from quizz.models.Base import Course  # Caso Course esteja em Base.py

JSON_FILE = "/app/quizz/questions.json"  # Ajuste o caminho do arquivo JSON conforme necessário

def carregar_cursos():
    """Cria cursos baseados nas opções disponíveis no JSON"""
    with open(JSON_FILE, "r", encoding="utf-8") as file:
        questions_data = json.load(file)

    cursos = set()
    for question_data in questions_data:
        for alt_data in question_data["alternatives"]:
            cursos.add(alt_data["recommended_course"])  # Coleta todos os cursos

    for curso in cursos:
        Course.objects.get_or_create(type=curso)

    print("Cursos carregados com sucesso!")

def carregar_perguntas():
    """Carrega perguntas e alternativas no banco de dados"""
    quiz, created = Quiz.objects.get_or_create(
        title="Teste Vocacional de Engenharia",
        description="Descubra qual engenharia combina mais com você!"
    )

    with open(JSON_FILE, "r", encoding="utf-8") as file:
        questions_data = json.load(file)

    for question_data in questions_data:
        question,_  = Question.objects.get_or_create(quiz=quiz, text=question_data["text"])

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
    carregar_cursos()
    carregar_perguntas()
