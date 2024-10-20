# expressbeats/models.py
from djongo import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        """Create and return a user with an email, username and password."""
        if not username:
            raise ValueError('The Username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """Create and return a superuser with an email, username and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)

class User(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)  # Unique username
    email = models.EmailField(unique=True)  # If you need an email field
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

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
