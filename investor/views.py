from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.mail import send_mail, EmailMessage
from django.apps import apps
from investor.models import Investor
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.conf import settings

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
                messages.error(request, 'Email or password is incorrect.')

        except Investor.DoesNotExist:
            messages.error(request, 'Email or password is incorrect.')

    return render(request, 'investor.html')


def get_approved(request):
    success_message = ''
    if request.method == 'POST':
        immigration_status = request.POST.get('immigration-status')
        full_address = request.POST.get('full-address')
        employment_status = request.POST.get('employment-status')
        credit_score = request.FILES.get('credit-score')

        # Send email with details
        email = EmailMessage(
            'New investor application',
            f'Immigration status: {immigration_status}\nLocation address: {full_address}\nEmployment status: {employment_status}',
            settings.EMAIL_HOST_USER,
            ['frankolayemi@gmail.com'],
        )
        email.attach(credit_score.name, credit_score.read(), credit_score.content_type)
        email.send()

        # Add success message to context
        success_message = 'Your details have been sent and are awaiting approval.'

    return render(request, 'investor/application.html', {'success_message': success_message})




