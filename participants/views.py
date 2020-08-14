from django.shortcuts import render, redirect
from django.contrib import messages

def login(request):
    if request.method == 'POST':
        messages.error(request, 'Testing error messages')
        return redirect('change_password')
    else:
        return render(request, 'participants/login.html')

def logout(request):
    return render(request, 'participants/logout.html')

def change_password(request):
    if request.method == 'POST':
        messages.error(request, 'Testing error messages')
        return redirect('change_password')
    else:
        return render(request, 'participants/change_password.html')
