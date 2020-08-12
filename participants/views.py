from django.shortcuts import render

def login(request):
    return render(request, 'participants/login.html')

def logout(request):
    return render(request, 'participants/logout.html')

def change_password(request):
    return render(request, 'participants/change_password.html')
