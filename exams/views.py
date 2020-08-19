from django.shortcuts import render, redirect
# from django.http import HttpResponseRedirect
from django.contrib import messages
from random import randint
from django.db import connection

from .models import Instruction, Question, Answer, Result

def instruction(request):
    instructions = Instruction.objects.all()
    context = {
        'instructions': instructions
    }
    return render(request, 'exams/instruction.html', context)

def question(request):
    questions = Question.objects.all().order_by('?')[:3]
    content = {
        'questions': questions
    }
    if request.method == 'POST':

        option_1 = request.POST.get('option_1', " ")
        option_2 = request.POST.get('option_2', False)
        option_3 = request.POST.get('option_3', False)
        option_4 = request.POST.get('option_4', False)
        option_5 = request.POST.get('option_5', False)
        question_text = request.POST.get('question_text', False)
        correct_option = request.POST.get('correct_option', False)
        
        savedata = Result(option_1=option_1,option_2=option_2,option_3=option_3,
                            option_4=option_4,option_5=option_5,question_text=question_text,correct_option=correct_option)
        
        savedata.save()
        messages.success(request, 'Submision Successiful')
        return redirect('question')        
    else:
        return render(request, 'exams/question.html', content)
