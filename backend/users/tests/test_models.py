from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError

# getting user model
User = get_user_model()

class UsersModelTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(email="test@example.com", username="test", password="test")
        user.name = "abbas"

        # testing part

        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.username, "test")
        self.assertEqual(user.name, "abbas")
        self.assertNotEqual(user.password, "test")
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_admin, False)

    def test_create_superuser(self):
        user = User.objects.create_superuser(email="test2@example.com", username="test2", password="test2") 
        user.name = "majid"

        # testing part

        self.assertEqual(user.email, "test2@example.com")
        self.assertEqual(user.username, "test2")
        self.assertNotEqual(user.password, "test2")
        self.assertEqual(user.name, "majid")
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_admin, True)

    def test_create_user_with_same_email_and_username(self):
        user = User.objects.return_user_intance(email="test3@example.com", username="test3@example.com", password="test3")

        # testing part

        with self.assertRaises(IntegrityError):
            user.save()        