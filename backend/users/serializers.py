from django.utils.text import gettext_lazy as _
from django.contrib.auth import get_user_model
from rest_framework import serializers

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
        return data