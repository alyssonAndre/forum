from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .serializers import QuestionSerializer
from quizz.models.Base import *
from quizz.models.Quiz import *

class QuestPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = "pages"
    max_page_size = 1

class QuestionListView(generics.ListAPIView):
    queryset = Question.objects.prefetch_related("alternatives").order_by('?')[:10]
    serializer_class = QuestionSerializer
    pagination_class = QuestPagination
    permission_classes = [IsAuthenticated]