from logging import raiseExceptions
from urllib import request
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import authentication, permissions
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS, BasePermission
from .models import *
from .serializers import *
from .email import sendOTP
# Create your views here.
class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


def homepage(request):
    template_name = 'index.html'
    return render(request, template_name)

class RegisterUser(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = RegitserSerializer(data=data)
            verify_user = User.objects.filter(email = data['email'])
            if not verify_user:
                if serializer.is_valid():
                    user = serializer.save()
                    sendOTP(user)
                    return Response({
                        'status': 200,
                        'message': 'Verification code sent on the mail address. Please check',
                        'data': serializer.data
                    })
            else:
                return Response({
                    'status': 400,
                    'message': 'You have already registerd',
                })
        except:
            return Response({
                    'status': 400,
                    'message': 'Oh! no. Something Went Wrong!',
                })
    def get(self, request):
        data = User.objects.all()
        serializer = UserSerializer(data, many=True)
        return Response({'success': True, 'payload': serializer.data})

class VerifyOTP(APIView):
    # permission_classes = (partial(MyPermission, ['GET', 'POST', 'HEAD']),)
    def post(self, request):
            data = request.data
            serializer = VerifySerializer(data = data)
            if serializer.is_valid():
                email = request.data['email']
                otp = request.data['otp']
                user = User.objects.filter(email=email).first()
                if user is None:
                    raise AuthenticationFailed('This Email address not found in our system.')
                if user.otp != otp:
                    raise AuthenticationFailed('otp does not match. Please try again.')
                else:
                    if not user.is_verified:
                        user.is_verified = True
                        user.save()
                        profile , created = UserProfile.objects.get_or_create(user = user, username=user.email)
                        profile.save()
                    # user = User.objects.get(email = serializer.data['email'])
                    # refresh = RefreshToken.for_user(user)
                        return Response({
                                'success': True,
                                'message': "You have successfully verified Email."
                            })
                    else:
                        return Response({
                                'success': True,
                                'message': "You have already verified Email."
                            })
            return Response({
                        'success': False,
                        'payload': 'Please Input validate data...',
                        
                    })



class LoginUserOTP(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data = data)
        if serializer.is_valid():
            email = request.data['email']
            password = request.data['password']
            user = User.objects.filter(email=email).first()
            if user is None:
                return Response({
                            'success': False,
                            'message': 'This Email address not found in our system.'
                        })
            if not user.check_password(password):
                return Response({
                            'success': False,
                            'message': 'Incorrect Password. Please try again!'
                        })
            else:
                if user.is_verified:
                    profile , created = UserProfile.objects.get_or_create(user = user, username=user.email)
                    profile.save()
                    user = User.objects.get(email = serializer.data['email'])
                    refresh = RefreshToken.for_user(user)
                    return Response({
                            'success': True,
                            'access': str(refresh.access_token)
                        })
                else:
                    return Response({
                        'success': False,
                        'message': 'You must be register first.',
                    })
        return Response({
                    'success': False,
                    'message': 'Please Input validate data...',
                })

class ChangePassword(APIView):
    def put(self, request, user):
        user = User.objects.get(user=user)
        serializer = ChangePasswordSerializer(user, data = request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({'success': False, 'message': 'password not match'})
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response({'success': True, 'message': 'password  changed'})

class UserProfileView(APIView):
    # permission_classes = [IsAuthenticated|ReadOnly]
    def get(self, request, user):
        try: 
            user_profile = UserProfile.objects.get(user__id=user)
            profile_serializer = ProfileSerializer(user_profile)
            return Response({'success': True, 'payload': profile_serializer.data})
        except:
            return Response({'success': False, 'message': 'Unauthenticted User'})
    def patch(self, request, user):
        try: 
            user_profile = UserProfile.objects.get(user__email=user)
            serializer = ProfileSerializer(user_profile, data = request.data, partial=True)
            if not serializer.is_valid():
                print(serializer.errors)
                return Response({
                    'success': False, 
                    'payload': serializer.errors, 
                    'message': 'Something went wrong'
                    })
            serializer.save()
            return Response({
                'success': True, 
                'payload': serializer.data, 
                'message': 'You have successfully updated profile.'
                })
        except:
            return Response({
                'success': False, 
                'message': 'Something Went Wrong..'
                })
