import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from backend.models import CustomUser
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        try:
            user = CustomUser.objects.get(email=email)
            if not user.is_active:
                messages.error(request, 'Account for this email is not active. Please contact the site owner.')
            else:
                user = authenticate(request, username=email, password=password)
                if user is not None:
                    auth_login(request, user)
                    return redirect('/')
                else:
                    messages.error(request, 'Invalid email or password.')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'login.html')

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')
        password_repeat = data.get('password_repeat')

        if password != password_repeat:
            return JsonResponse({'success': False, 'error': 'Passwords do not match'}, status=400)

        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({'success': True, 'message': 'User already exists'}, status=200)

        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_active=False
        )

        user.save()

        return JsonResponse({'success': True}, status=201)

    return render(request, 'register.html')

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = CustomUser.objects.get(email=email)
            # Here we would normally send an email, but for now, we just show a success message.
            messages.success(request, 'A link to reset your password would be sent to your email.')
        except CustomUser.DoesNotExist:
            messages.error(request, 'No account found with that email address.')

    return render(request, 'forgot_password.html')

@login_required(login_url='login')
def dashboard_view(request):
    return render(request, 'dashboard.html')

@login_required(login_url='login')
def accounts_view(request):
    return render(request, 'accounts.html')