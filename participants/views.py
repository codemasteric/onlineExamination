from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from . models import Participant

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

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        user = Participant.objects.get(user=user)
        print(user)
        # user_check = Participant.objects.filter(user=user.username)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        # Participant.objects.filter(years_ago__gt=5)
        # user.save()
        # login(request, user)
        return redirect('instruction')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
