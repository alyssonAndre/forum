from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .serializers import QuestionSerializer
from quizz.models.Base import *
from quizz.models.Quiz import *
from rest_framework.exceptions import ValidationError
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

        return selected_questions[:10]
