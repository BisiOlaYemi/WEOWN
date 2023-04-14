from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

def signup(request):
    if request.method == 'POST':
        # Extract form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Send registration email
        subject = 'Complete your registration'
        message = 'Click the following link to complete your registration: https://investors.weown.estate/complete-registration'
        from_email = 'contact@weown.estate'
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)

        # Save user data to database
        # ...

        # Redirect to success page
        return redirect('success')

    return render(request, 'signup.html')

def signin(request):
    try:
        if request.user.is_authenticated:
            return redirect('/board/')
        # message.info(request, 'Account not found')
        if request.method == 'POST':
            username= request.POST.get('username')
            password = request.POST.get('password')
            user_obj= User.objects.filter(username = username)
            if not user_obj.exists ():
                messages.info(request, 'Account not found')
                return redirect(request.META.get('HTTP_REFERER'))
            
            user_obj = authenticate(username = username, password = password)

            if user_obj and user_obj.is_superuser:
                login(request, user_obj)
                return redirect('/board/')
            
            messages.info(request, 'Invalid password')
            return redirect('/')
        return render(request, 'admin.html')
    except Exception as e:
       print(e)

def board(request):
    return render(request, 'board.html')

