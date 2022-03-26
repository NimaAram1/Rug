from django.utils.text import gettext_lazy as _
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .models import VerficationCode
from django.core.mail import send_mail
from .utils import give_code
from datetime import datetime
from rest_framework import status
from rest_framework.views import Response
import pytz

# time config
utc = pytz.UTC

# getting user model
User = get_user_model()

class RegisterationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, help_text=_("Enter a valid password"))
    repeated_password = serializers.CharField(write_only=True, required=True, help_text=_("Enter your password again"))
    
    def to_internal_value(self, data):
        email = data["email"] 
        if User.objects.filter(email=email, is_active=False).exists(): 
            user = User.objects.get(email=email)
            if VerficationCode.objects.filter(user=user).values("expire_date")[0]['expire_date'] < utc.localize(datetime.now()):
                VerficationCode.objects.filter(user=user).delete()
                verification_code = give_code()
                VerficationCode.objects.create(user=user, code=verification_code)
                send_mail("Verification Code", f"your code is: {verification_code}", "nima@gmail.com", [email])
                raise serializers.ValidationError({"message": _("Your account is already created but it isn't activated; the new code has been sent, please check your email"), "status": "A-C-1"})
            elif VerficationCode.objects.filter(user=user).values("expire_date")[0]['expire_date'] >= utc.localize(datetime.now()):
                raise serializers.ValidationError({"message": _("Your verification code is valid"), "status": "A-C-2"})
        return super().to_internal_value(data)
    
    class Meta:
        model = User
        fields = ["email", "username", "name", "password", "repeated_password"]
        extra_kwargs = {
            'email': {'help_text': _("Enter your email")},
            'username': {'help_text': _("Enter your username")},
            'name': {'help_text': _("Enter your name"), 'required': False, 'allow_blank': True},
        }

    
    def validate(self, data):
        if data["password"] and data["repeated_password"] and data["password"] != data["repeated_password"]:
            raise serializers.ValidationError(_("Password and repeated password must be the same"))
        if data["email"].strip() == data["username"].strip():
            raise serializers.ValidationError(_("Email and username must be different")) 
        return data

class LoginSerializer(serializers.ModelSerializer):
     email = serializers.EmailField(write_only=True, max_length=220, min_length=6, help_text=_("Enter your email"))
     password = serializers.CharField(write_only=True, required=True, help_text=_("Enter your password")) 
     class Meta:
        model = User
        fields = ["email", "password"]

     def validate(self, data):
        email = data["email"]
        password = data["password"]
        user = authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed(_("Your email or your password is incorrect"))
        elif not user.is_active:
            raise AuthenticationFailed(_("Your account has been disabled"))
        return super().validate(data) 
    



class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(write_only=True, required=True, help_text=_("Enter your refresh key for logout"))  

    default_error_messages = {
        "bad token": _("Your token doesn't valid")
    }

    def validate(self, data):
        self.token = data["refresh"]
        return data

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist() 
        except TokenError:
             self.fail("bad token")     

class ConfirmCodeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True, max_length=220, min_length=6, help_text=_("Enter your email"))
    class Meta:
        model = VerficationCode
        fields = ["email","code"]
        extra_kwargs = {
            'email': {'help_text': _("Enter your email")},
            'code': {'help_text': _("Enter your code")},
        }