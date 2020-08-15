from django.shortcuts import render

from .models import Instruction, Question, Answer
def instruction(request):
    instructions = Instruction.objects.all()
    context = {
        'instructions': instructions
    }
    return render(request, 'exams/instruction.html', context)

def question(request):
    questions = Question.objects.all()
    content = {
        'questions': questions
    }
    return render(request, 'exams/question.html', content)

