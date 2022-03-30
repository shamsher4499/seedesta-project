from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from .choices import *
from djmoney.models.fields import MoneyField
# Create your models here.
class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField( unique=True)
    mobile = models.CharField(max_length=10, null=True, blank=True)
    country_code = models.CharField(max_length=3, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    otp = models.CharField(max_length=6 ,null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    # last_login_time = models.DateTimeField(null=True, blank=True)
    # last_logout_time = models.DateTimeField(null=True, blank=True)
    terms_condition = models.BooleanField(default=True, verbose_name = "terms & conditions")
    rules_regulation = models.BooleanField(default=True, verbose_name = "rules & regulations")
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    def name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = "User Management"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=255, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='media/user/profile', blank=True, null=True)

    def __str__(self):
        return self.user.first_name

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=GOAL_CATEGORY, null=True, blank=True)
    goal_name = models.CharField(max_length=255, null=True, blank=True)
    goal_desc = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    
    def __str__(self):
        return self.user.first_name+ ' ' +self.goal_name
