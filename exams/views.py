from django.shortcuts import render, redirect
from django.db.models import Max
from django.contrib import messages
import random
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
from .models import Instruction, Question, Answer, Result
from django.contrib.auth.models import User

def instruction(request):
    instructions = Instruction.objects.all()
    context = {
        'instructions': instructions
    }
    return render(request, 'exams/instruction.html', context)

def question(request):
    if request.method == 'GET':
        max_id = Question.objects.all().aggregate(max_id=Max("id"))['max_id']
        user_id = request.user.id
        required = 2
        questions = []
        while True:
            user_done = Answer.objects.filter(participant_id=user_id).count()
            if user_done == required:
                messages.success(request, 'You are Done with your Exams')
                break
            pk = random.randint(1, max_id)
            question = Question.objects.filter(pk=pk).first()
            if question:
                try:
                    answered = Answer.objects.get(pk=pk,participant_id=user_id)
                except ObjectDoesNotExist:
                    questions.append(question)
                    break
        content = {
            'questions': questions
        }
        return render(request, 'exams/question.html', content)
    if request.method == 'POST':
        participant_id = request.user.id
        print(type(participant_id))
        question_id = request.POST['question_text']
        answer_text = request.POST['choice']
        answer = Answer(participant_id=participant_id, question_id=question_id, answer_text=answer_text) 
        answer.save()
        messages.success(request, 'Previous Answer Recorded')
        return redirect('question')        
    
