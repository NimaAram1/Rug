from rest_framework.views import APIView, Response
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework import status
from django.contrib.auth import authenticate
from .models import VerficationCode
from django.utils.text import gettext_lazy as _
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    RegisterationSerializer,
    LoginSerializer,
    LogoutSerializer,
    ConfirmCodeSerializer
)
from .utils import give_code

# getting user model
User = get_user_model()

class RegisterationApiView(APIView):
    """
    Get username, email, name, and password from the user
    and save it in the database
    """
    def post(self, request):
        if request.user.is_anonymous:
            data = RegisterationSerializer(data=request.data) 
            if data.is_valid():
                validated_data = data.validated_data
                del(validated_data["repeated_password"])
                user = User.objects.create_user(**validated_data)  
                verification_code = give_code()
                VerficationCode.objects.create(user=user, code=verification_code)
                send_mail("Verification Code", f"your code is: {verification_code}", "nima@gmail.com", [data.validated_data["email"]])
                return Response({
                "message": f'{data.validated_data["email"]} account was created successfully, your verification code has been sent to your email'
                }, status=status.HTTP_201_CREATED)
            
            else:
                return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "message": "You're already authorized"
            }, status=status.HTTP_400_BAD_REQUEST)   

class ConfirmCodeApiView(APIView):
    def post(self, request):
        data = ConfirmCodeSerializer(data=request.data)
        if data.is_valid():
            user = User.objects.get(email=data.validated_data["email"])
            if user.is_active:
                return Response({
                    "message": "Your account is already confirmed"
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                code = VerficationCode.objects.get(user=user)
                if code.code == data.validated_data["code"] and VerficationCode.objects.nonexpired().filter(user=user).exists():
                    user.is_active = True
                    user.save()
                    return Response({
                        "message": "Your account has been confirmed"
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "message": "Your code is incorrect or expired"
                    }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginApiView(generics.GenericAPIView):
    """
    Get email and password and authenticate user with those, Then
    generate access and refresh token for user 
    """

    serializer_class = LoginSerializer 

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        user = authenticate(email=email, password=password)
        tokens = RefreshToken.for_user(user)
        return Response({
            "access": str(tokens.access_token),
            "refresh": str(tokens)
        }, status=status.HTTP_200_OK)

class LogoutApiView(generics.GenericAPIView):
    """
    Get refresh token from the user(without user knows) and blacklist his/her key
    for logout  
    """
    
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)