from django.contrib import admin
from django.contrib.auth.models import User
from .models import Instruction, Question, Answer, Result, Monitor, Settings
from django.contrib import messages
from django.urls import path
from django.shortcuts import render, redirect
import csv
from django.http import HttpResponse




#export to csv file in admin
def export_as_csv_action(description="Export selected objects as CSV file",
                         fields=None, exclude=None, header=True):
    """
    This function returns an export csv action
    'fields' and 'exclude' work like in django ModelForm
    'header' is whether or not to output the column names as the first row
    """
    def export_as_csv(modeladmin, request, queryset):
        """
        Generic csv export admin action.
        based on http://djangosnippets.org/snippets/1697/
        """
        opts = modeladmin.model._meta
        field_names = set([field.name for field in opts.fields])
        if fields:
            fieldset = set(fields)
            field_names = field_names & fieldset
        elif exclude:
            excludeset = set(exclude)
            field_names = field_names - excludeset
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % str(opts).replace('.', '_')
        
        writer = csv.writer(response)
        if header:
            writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
        return response
    export_as_csv.short_description = description
    return export_as_csv


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
    search_fields = ['id']
    list_per_page = 25

class AnswerAdmin(admin.ModelAdmin):
    actions = [mark_answers]
    list_display = ('id', 'participant_id', 'question_id', 'answer_text', 'answer_value','question_text')
    list_display_links = ('id', 'participant_id','question_id', 'question_text')
    list_filter = ('answer_value', 'participant_id')
    search_fields = ['participant_id']
    list_per_page = 25

class ResultAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'marks', 'percentage')
    list_display_links = ('username',)
    list_filter = ('username', 'email', 'marks', 'percentage')
    list_per_page = 25
    search_fields = ['username', 'email', 'marks', 'percentage']
    

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('view-detail/', self.show_result),
        ]
        return my_urls + urls
    # def retrieve_result(self, request, queryset):
    #     self.show_result
    def show_result(modeladmin, request, queryset):
        data = []
        for user in queryset:
            participant_id = User.objects.get(username=user.username).id
            answers = Answer.objects.filter(participant_id=participant_id)
            quiz_answer_dict = {}
            for answer in answers:
                key = Question.objects.get(pk=answer.question_id).question_text
                # print(key)
                quiz_dict = quiz_answer_dict[key] = {}
                
                question = Question.objects.get(id=answer.question_id)
                quiz_dict["option_1"] = question.option_1
                quiz_dict["option_2"] = question.option_2
                quiz_dict["option_3"] = question.option_3
                quiz_dict["option_4"] = question.option_4
                quiz_dict["option_5"] = question.option_5
                quiz_dict["correct_option"] = question.correct_option
                quiz_dict["checked_option"] = answer.answer_text
                data.append(quiz_answer_dict)
            # print(quiz_answer_dict)
            

            print(data)
        
        payload = {"data": data}
        return render(
            request, "admin/results.html", payload
        )
    actions = [show_result]
class MonitorAdmin(admin.ModelAdmin):
    list_display = ('participant_id', 'questions_numbers', 'start_time', 'exams_ended' )
    list_display_links = ('participant_id',)
    list_filter = ('participant_id', 'questions_numbers', 'start_time', 'exams_ended')
    search_fields = ['participant_id']
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
