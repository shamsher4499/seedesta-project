from rest_framework import serializers
from .models import *

class RegitserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'mobile', 'country_code', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    terms_condition = serializers.BooleanField()
    rules_regulation = serializers.BooleanField()
    is_verified = serializers.BooleanField()
    is_active = serializers.BooleanField()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['user'] = UserSerializer(instance.user).data
        return rep

class VerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)