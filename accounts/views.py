from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import User, EmailOTP
from .utils import generate_otp


# Step 1: Enter Email & send OTP
def enter_email(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if not email:
            messages.error(request, " Please enter an email address")
            return render(request, 'accounts/auth.html', {'show_email': True})

        otp = generate_otp()
        EmailOTP.objects.create(email=email, otp=otp)
        request.session['otp_email'] = email

        # Send OTP via email
        subject = "Your OTP for Login"
        message = f"Hi and hello \n\nYour OTP for login is: {otp}\nrun before it crash."
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]

        try:
            send_mail(subject, message, from_email, recipient_list)
            messages.success(request, f" OTP sent to {email}")
        except Exception as e:
            messages.error(request, f" Could not send OTP: {e}")
            return render(request, 'accounts/auth.html', {'show_email': True})

        return render(request, 'accounts/auth.html', {
            'show_otp': True,
            'email': email
        })

    return render(request, 'accounts/auth.html', {'show_email': True})


# Step 2: Verify OTP
def verify_otp(request):
    if request.method == "POST":
        otp_input = request.POST.get("otp")
        email = request.session.get("otp_email")

        if not email:
            messages.error(request, "⚠️ Session expired. Enter email again.")
            return redirect("enter_email")

        if EmailOTP.objects.filter(email=email, otp=otp_input).exists():
            # Create user if not exists
            user, created = User.objects.get_or_create(email=email, defaults={
                'username': email.split('@')[0]
            })
            login(request, user)
            del request.session['otp_email']
            messages.success(request, f" Logged in as {user.email}")
            return redirect('home')
        else:
            messages.error(request, " Invalid OTP")
            return render(request, 'accounts/auth.html', {
                'show_otp': True,
                'email': email
            })
    return redirect('enter_email')


# Logout
def logout_view(request):
    logout(request)
    messages.success(request, " You have been logged out")
    return redirect('home')
