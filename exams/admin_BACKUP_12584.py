from django.contrib import admin
<<<<<<< HEAD

# Register your models here.
=======
from django.contrib.auth.models import User
from .models import Instruction, Question, Answer, Result, Monitor, Settings
from django.contrib import messages


def mark_answers(modeladmin, request, queryset):
    attendees = Monitor.objects.filter(questions_numbers__gt=0)
    for attendant in attendees:
        
        try:
            #get the user related details
            user = User.objects.get(pk=attendant.participant_id)
            username = user.username
            email = user.email
            #calculate the marks and percentages
            marks = Answer.objects.filter(participant_id=attendant.participant_id,answer_value=1).count()
            base_marks = Settings.objects.get(name="main").maximum_quiz_numbers
            percentage = ( marks / base_marks ) * 100
            #create the results
            result = Result(username=username,email=email,marks=marks,percentage=percentage)
            result.save()
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            messages.error(request, "Wait untill the participants have done the exams")
            continue
mark_answers.short_description = "Generate Results for this exams"



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
    actions = [mark_answers]
    list_display = ('id', 'participant_id', 'question_id', 'answer_text', 'answer_value')
    list_display_links = ('id', 'participant_id', 'answer_text', 'answer_value')
    list_filter = ('answer_text', 'answer_value', 'participant_id')
    list_per_page = 25

class ResultAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'marks', 'percentage')
    list_display_links = ('username',)
    list_filter = ('username', 'email', 'marks', 'percentage')
    list_per_page = 25

class MonitorAdmin(admin.ModelAdmin):
    list_display = ('participant_id', 'questions_numbers', 'start_time', 'exams_ended' )
    list_display_links = ('participant_id',)
    list_filter = ('participant_id', 'questions_numbers', 'start_time', 'exams_ended')
    list_per_page = 25

class SettingsAdmin(admin.ModelAdmin):
    list_display = ('maximum_quiz_numbers', 'exam_hours', 'exam_deadline' )
    list_display_links = ('maximum_quiz_numbers', 'exam_hours', 'exam_deadline')
    list_per_page = 25

admin.site.register(Instruction, InstructionAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Monitor, MonitorAdmin)
admin.site.register(Settings, SettingsAdmin)
>>>>>>> opiko
