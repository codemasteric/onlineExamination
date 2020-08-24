from django.shortcuts import render, redirect
from django.db.models import Max
from django.contrib import messages
import random
from datetime import datetime, time
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
from .models import Instruction, Question, Answer, Result, Monitor, Settings
from django.contrib.auth.models import User

def instruction(request):
    instructions = Instruction.objects.all()
    context = {
        'instructions': instructions
    }
    return render(request, 'exams/instruction.html', context)

def question(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            user_id = request.user.id
            #check if the exams was started
            try:
                start_time = Monitor.objects.get(participant_id=user_id).start_time
            except Monitor.DoesNotExist:
                start_time = Monitor(start_time=datetime.now(), participant_id=user_id)
                start_time.save()
            # if not start_time :
            #     start_time = Monitor(start_time=datetime.now())
            done = Monitor.objects.get(participant_id=user_id).questions_numbers
            max_no = Settings.objects.get(name="main").maximum_quiz_numbers
            if not(done > max_no):
                max_id = Question.objects.all().aggregate(max_id=Max("id"))['max_id']
                # required = 2
                questions = []
                while True:
                    # user_done = Answer.objects.filter(participant_id=user_id).count()
                    # if user_done == required:
                    #     messages.success(request, 'You are Done with your Exams')
                    #     break
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
            else:
                # exams_ended = Monitor(exams_ended=True)
                return render(request, 'exams/done.html')
        if request.method == 'POST':
            user_id = request.user.id
            participant_id = request.user.id
            print(type(participant_id))
            question_id = request.POST['question_text']
            answer_text = request.POST['choice']
            answer = Answer(participant_id=participant_id, question_id=question_id, answer_text=answer_text) 
            answer.save()
            user_done = Answer.objects.filter(participant_id=user_id).count()
            print(user_done)
            user_record = Monitor.objects.get(participant_id=user_id)
            user_record.questions_numbers = user_done
            user_record.save()
            messages.success(request, 'Previous Answer Recorded')
            return redirect('question')        
    
