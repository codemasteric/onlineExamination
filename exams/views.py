from django.shortcuts import render, redirect
from django.db.models import Max
from django.contrib import messages
import random
from datetime import datetime, time, timedelta
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
from .models import Instruction, Question, Answer, Result, Monitor, Settings
from django.contrib.auth.models import User


def deadline_passed(exam_deadline):
    present = datetime.date(datetime.now())
    return present < exam_deadline

def is_time_between(start_time, end_time, check_time=None):
    start_time = start_time.time()
    end_time = end_time.time()
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.time(datetime.now())
    print(type(check_time))
    if start_time < end_time:
        return check_time >= start_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= start_time or check_time <= end_time

def generate_exam_endtime(start_time, exam_hours):
    hours_added = timedelta(hours = float(exam_hours))
    end_time = start_time + hours_added
    return end_time



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
            #check if the exams was started, if it is not start monitoring
            try:
                start_time = Monitor.objects.get(participant_id=user_id).start_time
                end_time = Monitor.objects.get(participant_id=user_id).end_time
            except Monitor.DoesNotExist:
                exam_hours = Settings.objects.get(name="main").exam_hours
                start_time = datetime.now()
                end_time = generate_exam_endtime(start_time, exam_hours)
                print(type(end_time))
                monitor = Monitor(start_time=start_time, participant_id=user_id, end_time=end_time)
                monitor.save()
            
            #check if it is  deadline
            exam_deadline = Settings.objects.get(name="main").exam_deadline
            if not deadline_passed(exam_deadline):  
                # check if it is time already
                if is_time_between(start_time, end_time, check_time=None):

                    #obtain the number of questions attempted by the user and 
                    # the maximun allowed questions
                    done = Monitor.objects.get(participant_id=user_id).questions_numbers
                    max_no = Settings.objects.get(name="main").maximum_quiz_numbers  
                    #check for the number of questions done by the user,
                    # before generating another another quiz
                    if done < max_no:
                        max_id = Question.objects.all().aggregate(max_id=Max("id"))['max_id']
                        questions = []
                        while True:
                            pk = random.randint(1, max_id)
                            question = Question.objects.filter(pk=pk).first()
                            if question:
                                if done <= max_no:
                                    if Answer.objects.filter(question_id=pk).exists():
                                        continue                       
                                    questions.append(question) 
                                    break
                                else:
                                    return render(request, 'exams/done.html')

                        # try:
                        #     answered = Answer.objects.filter(pk=pk,participant_id=user_id)
                        # except ObjectDoesNotExist:
                        #     questions.append(question)    
            
                        content = {
                            'questions': questions
                        }
                        return render(request, 'exams/question.html', content)
                    else:
                        return render(request, 'exams/done.html')
                else:
                    return render(request, 'exams/timeout.html')
            else:
                return render(request, 'exams/deadline.html')
        if request.method == 'POST':
            user_id = request.user.id
            participant_id = request.user.id
            #obtain the number of questions attempted and required to be attempted
            done = Monitor.objects.get(participant_id=user_id).questions_numbers
            max_no = Settings.objects.get(name="main").maximum_quiz_numbers  
            #check if the user is done
            if done < max_no:
                print(type(participant_id))
                question_id = request.POST['question_text']
                answer_text = request.POST['choice']
                #mark the answers submitted by the user
                correct_option = Question.objects.get(id=question_id).correct_option
                if correct_option == answer_text:
                    answer_value = 1
                else:
                    answer_value = 0
                answer = Answer(participant_id=participant_id, question_id=question_id, answer_text=answer_text, answer_value=answer_value) 
                answer.save()
                #update the number of questions done by the user
                user_done = Answer.objects.filter(participant_id=user_id).count()
                print(user_done)
                user_record = Monitor.objects.get(participant_id=user_id)
                user_record.questions_numbers = user_done
                user_record.save()
                messages.success(request, 'Previous Answer Recorded')
                return redirect('question') 
            else:
                exams_ended = True
                user_record = Monitor.objects.get(participant_id=user_id)
                user_record.exams_ended = exams_ended
                user_record.save()
                return render(request, 'exams/done.html')

    else:
        return redirect('login')




