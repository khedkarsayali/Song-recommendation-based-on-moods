import os
import cv2
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from deepface import DeepFace
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.hashers import make_password
from home.models import User  # Ensure you have a custom user model defined

# Set up logging
logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'home.html')

def menu(request):
    return render(request, 'menu.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Check if passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        # Check if the username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('signup')

        # Create a new user
        new_user = User(
            username=username,
            email=email,
            password=make_password(password1)  # Hash the password
        )
        new_user.save()
        messages.success(request, "Signup successful! You can now log in.")
        return redirect('login')  # Redirect to the login page after successful signup

    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            return redirect('menu')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'login.html')

def live_emotion_detection(request):
    return render(request, 'live_emotion_detection.html')

from django.core.files.storage import FileSystemStorage

@csrf_exempt  # Use with caution; ensure appropriate security measures
def detect_emotion(request):
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_file = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.url(filename)  # This gives you a URL, not a local path

        # Use the local path for DeepFace analysis
        local_path = fs.path(filename)  # This gets the local file path

        try:
            # Perform emotion analysis on the uploaded image
            result = DeepFace.analyze(local_path, actions=['emotion'], enforce_detection=False)
            emotion = result[0]['dominant_emotion']
            return JsonResponse({'emotion': emotion})
        except Exception as e:
            return JsonResponse({"error": str(e)})

    return JsonResponse({"error": "Invalid request"})
