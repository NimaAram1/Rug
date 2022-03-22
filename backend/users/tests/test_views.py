from os import stat
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, smart_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.test.utils import override_settings
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework_simplejwt.exceptions import TokenError

# getting user model
User = get_user_model()

class AuthenticationTests(APITestCase):
    def setUp(self):
        login_user_url = reverse("users:login")
        login_user_data = {
            "email": "online@example.com",
            "password": "superpowerfulpassword"
        } 
        self.logout_url = reverse("users:logout")
        self.user = User.objects.create_user(email="online@example.com", username="online", password="superpowerfulpassword")
        self.user2 = User.objects.create_user(email="online2@example.com", username="online2", password="superpowerfulpassword")
        self.login_user = self.client.post(login_user_url, login_user_data) 
        self.tokens_for_logout = self.login_user.json()
        self.reset_password_uidb64 = urlsafe_base64_encode(smart_bytes(self.user.pk))
        self.reset_password_token = PasswordResetTokenGenerator().make_token(self.user)

    def test_registeration(self):
        registeration_url = reverse("users:registeration")
        registeration_data = {
            "email": "user@example.com",
            "username": "user",
            "password": "superpowerfulpassword",
            "repeated_password": "superpowerfulpassword"
        }
        registeration_response = self.client.post(registeration_url, registeration_data)
        
        # testing part

        self.assertEqual(registeration_response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        login_url = reverse("users:login")
        login_data = {
            "email": "online@example.com",
            "password": "superpowerfulpassword"
        }
        login_response = self.client.post(login_url, login_data)

        # testing part

        self.assertEqual(login_response.status_code, status.HTTP_200_OK)      

    def test_logout(self): 
        logout_data = {"refresh": self.tokens_for_logout["refresh"]}
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.tokens_for_logout["access"]))
        logout_response = self.client.post(self.logout_url, logout_data)

        # testing part

        self.assertEqual(logout_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_logout_with_bad_refresh_token(self):
        logout_data = {"refresh": "SuperTrashRefreshToken"}
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.tokens_for_logout["access"]))
        logout_response = self.client.post(self.logout_url, logout_data)
        
        # testing part

        self.assertEqual(logout_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_with_already_blacklisted_refresh_token(self): 
        logout_data = {"refresh": self.tokens_for_logout["refresh"]}
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.tokens_for_logout["access"]))
        logout_response = self.client.post(self.logout_url, logout_data)
        logout_response_second_try = self.client.post(self.logout_url, logout_data)
        
        # testing part

        self.assertEqual(logout_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(logout_response_second_try.status_code, status.HTTP_400_BAD_REQUEST)