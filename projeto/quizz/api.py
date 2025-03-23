from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import QuestionSerializer
from quizz.models.Base import *
from quizz.models.Quiz import *
import random


class QuestPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = "pages"
    max_page_size = 1


class QuestionListView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    pagination_class = QuestPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Obtém os IDs das perguntas já enviadas do frontend
        received_ids = self.request.query_params.getlist("received", [])

        try:
            # Converte para inteiros
            received_ids = list(map(int, received_ids))
        except ValueError:
            raise ValidationError(
                "Os IDs das perguntas devem ser números inteiros.")

        # Filtra perguntas que ainda não foram enviadas
        available_questions = Question.objects.exclude(id__in=received_ids)

        # Se não houver mais perguntas disponíveis, retorna todas novamente (reset)
        if not available_questions.exists():
            available_questions = Question.objects.all()

        # Seleciona até 10 perguntas aleatórias
        selected_questions = list(available_questions)
        random.shuffle(selected_questions)

        return selected_questions[:3]


class QuestionResultView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, quiz_id):
        user = request.user

        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            return Response({"error": "Quiz não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        best_course, score = UserAnswer.calculate_score(user, quiz)

        if best_course:
            return Response({
                "recommended_course": best_course,
                "score": score,
            })
        return Response({"message": "Nenhuma recomendação disponível."}, status=status.HTTP_400_BAD_REQUEST)


class SubmitAnswersView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        answers = request.data.get("answers", [])
        print("[LOG] Dados recebidos:", request.data)

        if not isinstance(answers, list) or not answers:
            print("[ERRO] Nenhuma resposta válida enviada.")
            return Response({"error": "Nenhuma resposta enviada."}, status=400)

        deleted_count, _ = UserAnswer.objects.filter(user=user).delete()
        print(f"[LOG] {deleted_count} respostas deletadas para o usuário {user}.")

        new_answers = []
        quiz = None
        for answer in answers:
            question_id = answer.get("question")
            alternative_id = answer.get("alternative")

            if not question_id or not alternative_id:
                print(f"[ERRO] Dados inválidos: question_id={question_id}, alternative_id={alternative_id}")
                return Response({"error": "Pergunta ou alternativa inválida."}, status=400)

            print(f"[LOG] Processando: question_id={question_id}, alternative_id={alternative_id}")

            try:
                question = Question.objects.get(id=question_id)
                alternative = Alternative.objects.get(id=alternative_id)
                quiz = question.quiz
            except Question.DoesNotExist:
                print(f"[ERRO] Pergunta {question_id} não encontrada.")
                return Response({"error": f"Pergunta {question_id} não encontrada."}, status=400)
            except Alternative.DoesNotExist:
                print(f"[ERRO] Alternativa {alternative_id} não encontrada.")
                return Response({"error": f"Alternativa {alternative_id} não encontrada."}, status=400)

            new_answers.append(UserAnswer(
                user=user,
                quiz=quiz,
                question=question,
                alternative=alternative
            ))

        if new_answers:
            UserAnswer.objects.bulk_create(new_answers)
            print(f"[LOG] {len(new_answers)} novas respostas inseridas.")

        if quiz:
            best_courses, score = UserAnswer.calculate_score(user, quiz)

            if isinstance(best_courses, list):
                return Response({
                    "message": "Seu perfil se relaciona com esses dois cursos!",
                    "recommended_courses": [course.name for course in best_courses],
                    "score": score
                })
            elif best_courses:
                return Response({
                    "message": "Respostas registradas com sucesso!",
                    "recommended_course": best_courses.name,
                    "score": score
                })

        return Response({"message": "Respostas registradas, mas nenhuma recomendação foi gerada."})
