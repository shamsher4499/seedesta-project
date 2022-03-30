from django.conf import settings
from django.core.mail import send_mail
import random
from .models import User

def sendOTP(user):
    subject = 'Email Verification Code'
    otp = random.randint(100000, 999999)
    message = f'Hii {user.first_name}\nYour OTP is {otp} for email verification'
    email_from = settings.EMAIL_HOST_USER
    send_mail( subject, message, email_from, [user.email] )
    print(send_mail( subject, message, email_from, [user.email] ))
    # user = RegisterUser.objects.get(email = email)
    user.otp = otp
    user.save()