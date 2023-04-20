from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.mail import send_mail, EmailMessage
from django.apps import apps
from investor.models import Investor
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseBadRequest


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

# accounts/views.py




class UserOrInvestorBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # First, try to authenticate the user
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        # If the user authentication fails, try the investor authentication
        if user is None:
            try:
                investor = Investor.objects.get(email=username)
                if investor.password == password:
                    user = investor.to_user()
            except Investor.DoesNotExist:
                investor = None

        # Return the authenticated user or investor
        return user or investor

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are logged in')
            return redirect('investboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'investboard.html')


# # investor/models.py
#     def to_user(self):
#         # Convert the Investor model to a User model
#         try:
#             user = User.objects.get(username=self.email)
#         except User.DoesNotExist:
#             user = User.objects.create_user(username=self.email, password=self.password)
#         return user
# investor/views.py

def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        investor = Investor.objects.filter(email=email, password=password).first()

        if investor is not None:
            user = investor.to_user()
            auth.login(request, user)
            messages.success(request, 'You are logged in')
            try:
                url = reverse('investboard')
            except Exception as e:
                return HttpResponseBadRequest(f"Error finding url for 'investboard': {e}")
            return redirect(url)
        else:
            messages.error(request, 'Email or password is incorrect.')
    
    return render(request, 'investboard.html')

def investboard(request):
    return render(request, 'investboard.html')


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




