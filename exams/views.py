from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from random import randint

from .models import Instruction, Question, Answer, Result
from .forms import QuestionForm

def instruction(request):
    instructions = Instruction.objects.all()
    context = {
        'instructions': instructions
    }
    return render(request, 'exams/instruction.html', context)

def question(request):
    questions = Question.objects.all().order_by('?')[:1]
    content = {
        'questions': questions
    }

    return render(request, 'exams/question.html', content)

def result(request):
    results = Result.objects.all()
    form = QuestionForm(request.POST)
    if request.method == 'POST':
        option_1 = request.POST['option_1']
        option_2 = request.POST['option_2']
        option_3 = request.POST['option_3']
        option_4 = request.POST['option_4']
        option_5 = request.POST['option_5']
        correct_option = request.POST['correct_option']
        if form.is_valid():
            savedata = Result(option_1=option_1,option_2=option_2,option_3=option_3,
                                                option_4=option_4,option_5=option_5,correct_option=correct_option)
            savedata.save()
            messages.SUCCESS(request, 'Submision Successiful')
            return redirect('exams/question.html')
        else:
            print('No Data Sumited')
            return render(request, 'exams/question.html', {'form': form})
            
    else:
        return render(request, 'exams/question.html')