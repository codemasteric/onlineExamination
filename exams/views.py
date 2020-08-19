from django.shortcuts import render, redirect
from django.db.models import Max
from django.contrib import messages
import random
from django.db import connection

from .models import Instruction, Question, Answer, Result

def instruction(request):
    instructions = Instruction.objects.all()
    context = {
        'instructions': instructions
    }
    return render(request, 'exams/instruction.html', context)

def question(request):
    max_id = Question.objects.all().aggregate(max_id=Max("id"))['max_id']
    while True:
        pk = random.randint(1, max_id)
        questions = Question.objects.filter(pk=pk).first()
        if questions:
            return questions
    content = {
        'questions': questions
    }
    if request.method == 'POST':

        option_1 = request.POST.get('option_1', " ")
        option_2 = request.POST.get('option_2', " ")
        option_3 = request.POST.get('option_3', " ")
        option_4 = request.POST.get('option_4', " ")
        option_5 = request.POST.get('option_5', " ")
        question_text = request.POST.get('question_text', " ")
        correct_option = request.POST.get('correct_option', " ")
        
        savedata = Result(option_1=option_1,option_2=option_2,option_3=option_3,
                            option_4=option_4,option_5=option_5,question_text=question_text,correct_option=correct_option)
        
        savedata.save()
        messages.success(request, 'Submision Successiful')
        return redirect('question')        
    else:
        return render(request, 'exams/question.html', content)
