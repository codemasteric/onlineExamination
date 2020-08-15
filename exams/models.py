from django.db import models

from participants.models import Participant

class Instruction(models.Model):
    title = models.CharField(max_length=500, blank=True)
    content = models.TextField(blank=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    question_text = models.TextField(blank=True)
    option_1 = models.TextField(blank=True)
    option_2 = models.TextField(blank=True)
    option_3 = models.TextField(blank=True)
    option_4 = models.TextField(blank=True)
    option_5 = models.TextField(blank=True)
    correct_option = models.TextField(blank=True)

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    participant_id = models.ForeignKey(Participant, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField(blank=True)
    answer_value = models.IntegerField(blank=True)

    def __str__(self):
        return self.answer_text


