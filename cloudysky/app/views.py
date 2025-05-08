from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.urls import reverse
from datetime import datetime

# Create your views here.
def index(request):
    # Get current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create context with time and team members
    context = {
        'current_time': current_time,
        'team_members': [
            {'name': 'Samuel Shen', 'bio': 'Mathematics and Computer Science Student'}
        ]
    }

    return render(request, 'app/index.html', context)

def new_user_form(request):
    # Only accept GET requests for this view
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    return render(request, 'app/new_user_form.html')

def create_user(request):
    # Only accept POST requests for this view
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    # Get form data
    user_name = request.POST.get('user_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    is_admin = request.POST.get('is_admin') == '1'

    # Validate data
    if not user_name or not email or not password:
        return JsonResponse({'status': 'error', 'message': 'Missing required fields'}, status=400)

    # Check if email is already used
    if User.objects.filter(email=email).exists():
        return JsonResponse({'status': 'error', 'message': 'Email already in use'}, status=400)

    # Create user
    try:
        user = User.objects.create_user(
            username=user_name,
            email=email,
            password=password
        )

        # Set last name if provided
        if last_name:
            user.last_name = last_name

        # Set user as staff if is_admin is True
        if is_admin:
            user.is_staff = True

        user.save()

        # Log the user in
        login(request, user)

        # Return success with 200 status code
        return HttpResponse("User created successfully", status=200)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
