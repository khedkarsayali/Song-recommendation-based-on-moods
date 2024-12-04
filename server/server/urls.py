from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from home.views import (
    home,
    signup,
    login,
    menu,
    admin,
    live_emotion_detection,
    delete_user,
    admin_login,
    detect_emotion,
    get_top_songs_by_emotion_view,
)

urlpatterns = [
    path('', home, name='home'), 
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('menu/', menu, name='menu'),
    path('admin/', admin, name='admin'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('live-emotion-detection/', live_emotion_detection, name='live_emotion_detection'),
    path('admin_login/', admin_login, name='admin_login'),
    path('detect-emotion/', detect_emotion, name='detect_emotion'),
    path('get-songs/<str:emotion>/', get_top_songs_by_emotion_view, name='get_top_songs_by_emotion'),
]

# Add static route for media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
