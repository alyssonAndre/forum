from django.contrib import admin
from .models import Quiz, Question, Alternative, UserAnswer
from .models.Base import Course



class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title',)
    list_filter = ('title',)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz')
    search_fields = ('text',)
    list_filter = ('quiz',)

class AlternativeAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'score', 'recommended_course')
    search_fields = ('text',)
    list_filter = ('question', 'recommended_course')

class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'question', 'alternative', 'data')
    search_fields = ('user__username', 'quiz__title', 'question__text')
    list_filter = ('quiz', 'question', 'user')


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'description',)
    search_fields = ('name', 'type', 'description')
    list_filter = ('type', 'is_deleted')
    ordering = ('name',)


# Registro de todos os modelos
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Alternative, AlternativeAdmin)
admin.site.register(UserAnswer, UserAnswerAdmin)
admin.site.register(Course, CourseAdmin)
