from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db import transaction

from rest_framework import serializers, status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from djoser.serializers import UserCreateSerializer, UserSerializer


User = get_user_model()

# 987654321@


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta(UserCreateSerializer.Meta):
        fields = ["id", "email", "password", "username", "image"]


    def create(self, validated_data):
        email = validated_data['email']
        email = email.lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError({"email": "Account with this email already exists."})

        validated_data['email'] = email

        try:
            with transaction.atomic():
                user = super().create(**validated_data)

                user.save()

                ### Send OTP Email
                # send_otp_via_email(email)

        except Exception as e:
            raise serializers.ValidationError({"error":str(e)})

        return user



# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
#     def validate(self, attrs):
#         data = super().validate(attrs)

#         # Check if the user is active
#         user = self.user

#         refresh = RefreshToken.for_user(user)

#         return {
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#         }