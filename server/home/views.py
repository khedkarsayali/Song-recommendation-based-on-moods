from django.contrib.auth.hashers import check_password
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from deepface import DeepFace
from django.shortcuts import render, redirect , get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.hashers import make_password
from home.models import User  # Ensure you have a custom user model defined


def live_emotion_detection(request):
    return render(request, 'live_emotion_detection.html')

from django.core.files.storage import FileSystemStorage

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

from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login as auth_login
from django.contrib import messages
from home.models import User  # Make sure this points to your user model

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username).first()

        if user and check_password(password, user.password):  # Verify hashed password
            auth_login(request, user)
            return redirect('menu')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'login.html')

import pandas as pd
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from deepface import DeepFace
from django.views.decorators.csrf import csrf_exempt
import logging
SPOTIFY_DATASET_PATH = r'C:\Users\Admin\Documents\College\Sem 5\AI prj\3D-Structures-Generation-from-2D\server\genres_v2.csv'

try:
    spotify_data = pd.read_csv(SPOTIFY_DATASET_PATH)
    print(spotify_data.head())
except Exception as e:
    print(f"An error occurred: {e}")

# Example mapping of emotions to genres; you can modify this as needed
emotion_to_genre = {
    'happy': 'pop',
    'sad': 'dark trap',  # assuming "Dark Trap" corresponds to sad
    'angry': 'rock',
    'surprise': 'electronic',
    'disgust': 'classical',
    'fear': 'ambient'
}
from django.http import JsonResponse
import pandas as pd

# Assuming you have loaded the Spotify dataset as `spotify_data` and defined `emotion_to_genre` as shown before

def fetch_top_songs_by_emotion(emotion):
    # Get the genre based on the detected emotion
    genre = emotion_to_genre.get(emotion.lower(), None)
    
    if genre:
        # Filter songs based on the genre
        filtered_songs = spotify_data[spotify_data['genre'].str.contains(genre, case=False, na=False)]
        
        # Get top 10 songs based on a specific criteria (e.g., energy)
        top_songs = filtered_songs.nlargest(10, 'energy')  # Assuming 'energy' as a sorting criteria

        # Convert to a list of dictionaries with only 'song_name' and 'uri'
        top_songs_list = top_songs[['song_name', 'uri']].to_dict(orient='records')

        # Print songs to the terminal for testing
        print("Top Songs for Emotion '{}':".format(emotion))
        for song in top_songs_list:
            print("Song Name: {}, URI: {}".format(song['song_name'], song['uri']))

        return top_songs_list
    else:
        return []  # Return an empty list if no genre matches



def get_top_songs_by_emotion_view(request, emotion):
    # Call your existing logic to get top songs by emotion
    top_songs = fetch_top_songs_by_emotion(emotion)  # Call the renamed function
    
    if top_songs:
        return JsonResponse({'top_songs': top_songs})
    else:
        return JsonResponse({'error': 'No songs found for this emotion.'}, status=404)

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

def admin(request):
    users = User.objects.all()  # Fetch all users from the database
    return render(request, 'admin.html', {'users': users})

def delete_user(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(User, id=user_id)  # Get the user by ID
        user.delete()  # Delete the user
        return redirect('admin')
    
ADMIN_PASSWORD = 'abcd1234'

def admin_login(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        if password == ADMIN_PASSWORD:
            # Password is correct, redirect to admin dashboard
            return redirect('admin')
        else:
            # Password is incorrect, return error message
            return render(request, 'admin_login.html', {'error': 'Incorrect password. Please try again.'})
    return render(request, 'admin_login.html')