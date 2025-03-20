from django.contrib import admin
from .models import Quiz, Question, Alternative, UserAnswer
from .models.Base import Course


# Registro do modelo Quiz
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title',)
    list_filter = ('title',)

# Registro do modelo Question
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz')
    search_fields = ('text',)
    list_filter = ('quiz',)

# Registro do modelo Alternative
@admin.register(Alternative)
class AlternativeAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'score', 'recommended_course')
    search_fields = ('text',)
    list_filter = ('question', 'recommended_course')

# Registro do modelo UserAnswer
@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'question', 'alternative', 'data')
    search_fields = ('user__username', 'quiz__title', 'question__text')
    list_filter = ('quiz', 'question', 'user')


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'description',)
    search_fields = ('name', 'type', 'description')
    list_filter = ('type', 'is_deleted')
    ordering = ('name',)

admin.site.register(Course, CourseAdmin)
