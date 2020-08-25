from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.models import User
from . models import Participant

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, user)
            return redirect('instruction')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('login')
    else:
        return render(request, 'participants/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, "You are now logged out")
        return redirect('login')

def change_password(request):
    # if request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['user']
            print(username)
            # username = user.username
            password = request.POST['password']
            password2 = request.POST['password2']
            #check if password match
            if password == password2:
                user =  User.objects.get(username=username)
                user.set_password(password2)
                # messages.success(request, 'Your password has been changed successfully')
                
                user.is_active = True
                user.save()
                auth.login(request, user)
                return render(request, 'participants/update_success.html')
            else:
                messages.error(request, 'Passwords donot match')
                return redirect('change_password')
        else:
            return render(request, 'participants/change_password.html')

    # else:
    #     return redirect('login')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        real_user = User.objects.get(pk=uid)
        user = Participant.objects.get(user=real_user)
        # print(user)
        # user_check = Participant.objects.filter(user=user.username)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        # participant = Participant.objects.filter(user=user.username)
        # user.is_active = True
        # auth.login(request, real_user)
        context = {
            "user": real_user
        }
        return render(request, 'participants/change_password.html', context)
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
