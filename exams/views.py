from django.shortcuts import render

def instruction(request):
    return render(request, 'exams/instruction.html')

def question(request):
    return render(request, 'exams/question.html')

