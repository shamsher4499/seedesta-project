from django.urls import path
from . import views
from .views import RegisterUser, LoginUserOTP, UserProfileView, VerifyOTP, ChangePassword

urlpatterns = [
    path('', views.homepage, name='home'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUserOTP.as_view(), name='login'),
    path('verify/', VerifyOTP.as_view(), name='verify'),
    path('user-profile/<str:user>/', UserProfileView.as_view()),
    path('change-password/<int:user>/', ChangePassword.as_view()),
    
]