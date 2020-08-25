from django.shortcuts import render, redirect

def instruction(request):
    if request.user.is_authenticated:
        return render(request, 'exams/instruction.html')
    else:
        return redirect('login')

def question(request):
    if request.user.is_authenticated:
        return render(request, 'exams/question.html')
    else:
        return redirect('login')
    

