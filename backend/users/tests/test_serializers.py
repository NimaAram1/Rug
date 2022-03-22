from django.test import TestCase
from django.contrib.auth import get_user_model
from ..serializers import (
    RegisterationSerializer,
    LoginSerializer,
    LogoutSerializer
)

# getting user model
User = get_user_model()

class TestRegisterationSerializer(TestCase):
    def test_serialize_user(self):
        user = User.objects.create_user(email="test@example.com", username="test", password="testbadtest")
        serialized_user = RegisterationSerializer(user)

        # testing part

        self.assertEqual(
            User.objects.get(username=serialized_user.data["username"]), user, "Serializer didn't work")
        self.assertEqual(
            serialized_user.data["email"], "test@example.com", "Serializer didn't work")

class TestLoginSerializer(TestCase):
    def test_login_via_email(self):
        User.objects.create_user(email="test@example.com", username="test", password="superpowerfulpassword")
        serialized_user = LoginSerializer(data={"email":"test@example.com", "password":"superpowerfulpassword"})
        
        # testing part
        
        self.assertTrue(serialized_user.is_valid())

class TestLogoutSerializer(TestCase):
    def test_logout(self):
        serialized_refresh_key = LogoutSerializer(data={"refresh":"eyJhbGciOiJIUzI1\
        NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiw\
        iaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"})

        # testing part

        self.assertTrue(serialized_refresh_key.is_valid())