from multiprocessing import AuthenticationError
from django.utils.text import gettext_lazy as _
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

# getting user model
User = get_user_model()

class RegisterationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, help_text=_("Enter a valid password"))
    repeated_password = serializers.CharField(write_only=True, required=True, help_text=_("Enter your password again"))
    
    
    class Meta:
        model = User
        fields = ["email", "username", "name", "password", "repeated_password"]
        extra_kwargs = {
            'email': {'help_text': _("Enter your email")},
            'username': {'help_text': _("Enter your username")},
            'name': {'help_text': _("Enter your name")}
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

    def validate(self, data):
        self.token = data["refresh"]
        return data

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist() 
        except TokenError:
            raise AuthenticationFailed(_("Your token isn't valid"))       