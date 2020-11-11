from django.db import models
from random import randint

from participants.models import Participant

class Instruction(models.Model):
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField(blank=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    question_text = models.TextField(blank=True)
    option_1 = models.CharField(max_length=200,blank=True)
    option_2 = models.CharField(max_length=200,blank=True)
    option_3 = models.CharField(max_length=200,blank=True)
    option_4 = models.CharField(max_length=200,blank=True)
    option_5 = models.CharField(max_length=200,blank=True)
    correct_option = models.CharField(max_length=200,blank=True)

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    participant_id = models.IntegerField()
    question_id = models.IntegerField()
    answer_text = models.CharField(max_length=200, blank=True)
    answer_value = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return self.answer_text

class Result(models.Model):
    username = models.CharField(max_length=200,blank=True)
    email = models.EmailField(max_length=200,blank=True)
    marks = models.IntegerField(blank=True)
    percentage = models.IntegerField(blank=True)

    def __str__(self):
        return self.username

class Monitor(models.Model):
    participant_id = models.IntegerField(null=True, blank=True)
    questions_numbers = models.IntegerField(null=True, blank=True, default=0)
    start_time = models.DateTimeField(auto_now=False, null=True, blank=True)
    end_time = models.DateTimeField(auto_now=False, null=True, blank=True)
    exams_ended = models.BooleanField(default=False, null=True, blank=True)

class Settings(models.Model):
    maximum_quiz_numbers = models.IntegerField(null=True, blank=True, default=1)
    exam_hours = models.DecimalField(max_digits=2, decimal_places=1, null=True)
    exam_deadline = models.DateField(auto_now=False, null=True, blank=True)
    name = models.CharField(max_length=20, default='main')
    begin = models.BooleanField(default=False)



