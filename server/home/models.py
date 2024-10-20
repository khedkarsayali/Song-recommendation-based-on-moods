# expressbeats/models.py
from djongo import models

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

class Emotion(models.Model):
    user_id = models.IntegerField()  # Link to your User model if needed
    emotion = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     abstract = False  # Ensure this is not abstract for Djongo compatibility

    def __str__(self):
        return f"{self.user_id} - {self.emotion} at {self.timestamp}"
