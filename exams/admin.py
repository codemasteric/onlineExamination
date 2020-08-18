from django.contrib import admin

from .models import Instruction, Question, Answer, Result

class InstructionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content')
    list_display_links = ('id', 'title')
    list_filter = ('title', )
    list_per_page = 25

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_text', 'correct_option')
    list_display_links = ('id', 'question_text')
    list_filter = ('question_text', 'correct_option')
    list_per_page = 25

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'participant_id', 'question_id', 'answer_text', 'answer_value')
    list_display_links = ('id', 'participant_id', 'answer_text', 'answer_value')
    list_filter = ('answer_text', 'answer_value', 'participant_id')
    list_per_page = 25

class ResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'participant_id', 'option_1', 'option_2', 'option_3', 'option_4', 'option_5', 'correct_option', 'score')
    list_display_links = ('id', 'correct_option', 'score')
    list_filter = ('correct_option', 'score')
    list_per_page = 25

admin.site.register(Instruction, InstructionAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Result, ResultAdmin)
