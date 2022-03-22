from django.test import TestCase
from ..forms import UserCreateFormAdmin, UserChangeFormAdmin
from django.contrib.auth import get_user_model

# getting user model
User = get_user_model()

class TestUserCreateAdminForm(TestCase):
    def test_valid_data_user_create(self):
        form = UserCreateFormAdmin(data={"email":"test50@example.com", "username":"test", "password":"superpassword2000", "repeated_password":"superpassword2000"})
        self.assertTrue(form.is_valid())


    def test_invalid_data_user_create(self):
        form = UserCreateFormAdmin(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

class TestUserChangeAdminForm(TestCase):
    def test_valid_data_user_change(self):
        user_object = User.objects.create_user(email="test@example.com", username="test", password="superpassword")
        form = UserChangeFormAdmin(instance=user_object)
        self.assertTrue(form.is_valid)


    def test_invalid_data_user_change(self):
        form = UserChangeFormAdmin(data={"email":"test@example.com", "password":"superpassword"})
        with self.assertRaises(KeyError): 
            form.is_valid()
        self.assertEqual(len(form.errors), 1) 