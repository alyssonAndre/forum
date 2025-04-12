from rest_framework import generics
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

    def get_queryset(self):
        received_ids = self.request.query_params.getlist("received", [])
        user = self.request.user

        if user.profile.attempts >=3:
            raise ValidationError(
                "Você já atingiu o limite de 3 tentativas para o teste vocacional."
            )

        try:
            received_ids = list(map(int, received_ids))
        except ValueError:
            raise ValidationError(
                "Os IDs das perguntas devem ser números inteiros.")

        available_questions = Question.objects.exclude(id__in=received_ids)

        if not available_questions.exists():
            available_questions = Question.objects.all()

        selected_questions = list(available_questions)
        random.shuffle(selected_questions)

        return selected_questions[:10]


class QuestionResultView(APIView):

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

    def post(self, request):
        user = request.user
        answers = request.data.get("answers", [])

        if user.profile.attempts >= 3:
            return Response({
                "error": "Você já atingiu o limite de 3 tentativas para o teste vocacional."
                         "Nào é possivel realizer o teste novamente"
            })

        if not isinstance(answers, list) or not answers:
            return Response({"error": "Nenhuma resposta enviada."}, status=400)

        deleted_count, _ = UserAnswer.objects.filter(user=user).delete()

        new_answers = []
        quiz = None
        for answer in answers:
            question_id = answer.get("question")
            alternative_id = answer.get("alternative")

            if not question_id or not alternative_id:
                return Response({"error": "Pergunta ou alternativa inválida."}, status=400)


            try:
                question = Question.objects.get(id=question_id)
                alternative = Alternative.objects.get(id=alternative_id)
                quiz = question.quiz
            except Question.DoesNotExist:
                return Response({"error": f"Pergunta {question_id} não encontrada."}, status=400)
            except Alternative.DoesNotExist:
                return Response({"error": f"Alternativa {alternative_id} não encontrada."}, status=400)

            new_answers.append(UserAnswer(
                user=user,
                quiz=quiz,
                question=question,
                alternative=alternative
            ))

        if new_answers:
            UserAnswer.objects.bulk_create(new_answers)
            user.profile.attempts += 1
            user.profile.save()

        if quiz:
            best_courses, score = UserAnswer.calculate_score(user, quiz)

            if isinstance(best_courses, list):
                return Response({
                    "message": "Seu perfil se relaciona com esses dois cursos!",
                    "recommended_courses": [course.name for course in best_courses],
                    "score": score
                })
            elif best_courses:
                if hasattr(user, "profile"):
                    user.profile.courses = best_courses
                    user.profile.save()

                return Response({
                    "message": "Respostas registradas com sucesso!",
                    "recommended_course": best_courses.name,
                    "score": score
                })

        return Response({"message": "Respostas registradas, mas nenhuma recomendação foi gerada."})
