from django import forms

from .models import Question, Answer, Result

class QuestionForm(forms.ModelForm):
    option_1 = forms.CharField(max_length=200)
    option_2 = forms.CharField(max_length=200)
    option_3 = forms.CharField(max_length=200)
    option_4 = forms.CharField(max_length=200)
    option_5 = forms.CharField(max_length=200)
    correct_option = forms.CharField(max_length=200)
    class Meta:
        model = Result
        fields = ('option_1', 'option_2', 'option_3', 'option_4', 'option_5', 'correct_option')