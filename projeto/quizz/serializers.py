from rest_framework import serializers
from quizz.models.Base import *
from quizz.models.Quiz import *

class AlternativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alternative
        fields = "__all__"

class QuestionSerializer(serializers.ModelSerializer):
    alternatives = AlternativeSerializer(many=True, read_only=True)
    class Meta:
        model = Question
        fields = "__all__"

    def get_alternatives(self, obj):
        """Retorna no máximo 5 alternativas para cada pergunta"""
        return AlternativeSerializer(obj.alternatives.all()[:5], many=True).data

class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = '__all__'