from rest_framework import  serializers
from rest_framework.permissions import IsAuthenticated
from django.db import models
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from .models import CustomUser
# Register serializer
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        lower_email = value.lower()
        if CustomUser.objects.filter(email__iexact=lower_email).exists():
            raise serializers.ValidationError("email alrady attached to a exsisting user")
        return lower_email

    class Meta:
        model = CustomUser
        fields = ('username','password','first_name', 'last_name','email')
        extra_kwargs = {
            'password':{'write_only': True},
        }
    def create(self, validated_data):
        user = CustomUser.objects.create_user(validated_data['username'], email = validated_data['email'] ,  password = validated_data['password']  ,first_name=validated_data['first_name'],  last_name=validated_data['last_name'])
        return user

# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'