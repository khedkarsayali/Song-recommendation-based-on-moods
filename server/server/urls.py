# myapp/urls.py
from django.urls import path
from home.views import home,signup,login,menu,admin,live_emotion_detection,delete_user, admin_login

urlpatterns = [
    path('', home, name='home'), 
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('menu/', menu, name='menu'),
    path('admin/', admin, name='admin'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('live-emotion-detection/', live_emotion_detection, name='live_emotion_detection'),
    path('admin_login/',admin_login, name='admin_login'),
]
