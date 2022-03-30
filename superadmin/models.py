from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import *
from .choices import *
import uuid
# Create your models here.

class User(AbstractUser):
    username = None
    email = models.EmailField( unique=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    mobile = models.CharField(max_length=255, null=True, blank=True)
    otp = models.CharField(max_length=6 ,null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.CharField(max_length=50, unique=True, default=uuid.uuid4)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
        
    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = "Super Admin"


class Goal(models.Model):
    goal_name = models.CharField(max_length=255, blank=True, null=True)
    goal_desc = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)


    # def __str__(self):
    #     return self.goal_name

class Customer(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    mobile = models.CharField(max_length=255, null=True, blank=True, unique=True)

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []

    # objects = UserManager()
    
    def __str__(self):
        return self.email

class SocialIcon(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    icon = models.ImageField(upload_to='media', null=True, blank=True)
    link = models.URLField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name