from django.shortcuts import render, redirect
from django.core.mail import send_mail

def signup(request):
    if request.method == 'POST':
        # Extract form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Send registration email
        subject = 'Complete your registration'
        message = 'Click the following link to complete your registration: https://investors.weown.estate/complete-registration'
        from_email = '@weown.estate'
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)

        # Save user data to database
        # ...

        # Redirect to success page
        return redirect('success')

    return render(request, 'signup.html')



