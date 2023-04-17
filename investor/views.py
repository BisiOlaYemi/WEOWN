from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.apps import apps
from investor.models import Investor
from django.contrib import messages
from django.contrib.auth import authenticate, login

def signup(request):
    Investor = apps.get_model('investor', 'Investor')
    
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        investor = Investor(name=name, email=email, password=password)
        investor.save()

        # send email notification
        subject = 'Welcome to Our Investment Platform'
        message = f'Dear {name},\n\nThank you for registering as an investor on our platform.'
        from_email = 'marketing@weown.estate'
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        return HttpResponseRedirect('/success/')
    return render(request, 'signup.html')

def success(request):
    return render(request, 'success.html')

def signin(request):
    Investor = apps.get_model('investor', 'Investor')
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            investor = Investor.objects.get(email=email)

            if investor.password == password:
                return render(request, 'investboard.html')

            else:
                messages.error(request, 'Incorrect password')

        except Investor.DoesNotExist:
            messages.error(request, 'Email not recognised')

    return render(request, 'investor.html')
