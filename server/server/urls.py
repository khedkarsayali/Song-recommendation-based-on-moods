# myapp/urls.py
from django.urls import path
from home.views import home,signup,login,menu,detect_emotion,live_emotion_detection

urlpatterns = [
    path('', home, name='home'), 
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('menu/', menu, name='menu'),
    path('detect-emotion/', detect_emotion, name='detect_emotion'),
    path('live-emotion-detection/', live_emotion_detection, name='live_emotion_detection'),
]
